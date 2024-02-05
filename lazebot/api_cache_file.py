import json
import os
from lazebot.api_cache import ApiCache


class ApiCacheFile(ApiCache):

    def __init__(self, base_paths=("../filecache/", "/filecache/")):
        self.basePath = None
        for base_path in base_paths:
            if os.path.exists(base_path):
                self.basePath = base_path
            else:
                print(f"Couldn't find cache path {base_path} in {os.getcwd()}")

    def fetch_player(self, ally_code: str):
        if self.basePath:
            try:
                with open(f"{self.basePath}/{ally_code}.json") as f:
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
                with open(f"{self.basePath}/{guild_id}.json") as f:
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
