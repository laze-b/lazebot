import json
import os
from datetime import datetime, timezone
from lazebot.api_cache import ApiCache

DEFAULT_TTL_SECONDS = 24 * 60 * 60  # default to one day


class ApiCacheFile(ApiCache):

    def __init__(self, ttl_seconds=DEFAULT_TTL_SECONDS, base_paths=None):
        if base_paths is None:
            base_paths = ["filecache/"]
        self.ttlSeconds = ttl_seconds
        self.basePath = None
        for base_path in base_paths:
            if self.basePath is None:
                if os.path.exists(base_path):
                    self.basePath = base_path
                else:
                    print(f"Couldn't find cache dir {base_path}")
        if self.basePath is None:
            print(f"No viable cache dirs found in in {os.getcwd()}.")
            raise FileNotFoundError()

    def __expired__(self, location):
        if self.ttlSeconds < 0:  # infinite TTL, never expires
            return False
        else:
            currtime_seconds = (datetime.now(timezone.utc) - datetime.fromtimestamp(0, timezone.utc)).total_seconds()
            return currtime_seconds - os.path.getmtime(location) > self.ttlSeconds

    def fetch_player(self, ally_code: str):
        if self.basePath:
            try:
                location = f"{self.basePath}/{ally_code}.json"
                if not self.__expired__(location):
                    with open(location) as f:
                        return json.load(f)
            except FileNotFoundError:
                pass
        return None

    def add_player(self, ally_code: str, player):
        if self.basePath:
            try:
                with open(f"{self.basePath}/{ally_code}.json", "w") as f:
                    f.write(json.dumps(player))
                    return
            except FileNotFoundError:
                pass

    def fetch_guild(self, guild_id: str):
        if self.basePath:
            try:
                location = f"{self.basePath}/{guild_id}.json"
                if not self.__expired__(location):
                    with open(location) as f:
                        return json.load(f)
            except FileNotFoundError:
                pass
        return None

    def add_guild(self, guild_id: str, guild):
        if self.basePath:
            try:
                with open(f"{self.basePath}/{guild_id}.json", "w") as f:
                    f.write(json.dumps(guild))
                    return
            except FileNotFoundError:
                pass
