import os
from dotenv import load_dotenv
from discord import app_commands
import discord
import report_generator
import logging


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        guild_ids = os.getenv("GUILD_IDS")
        for guild_id in guild_ids.split(","):
            my_guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=my_guild)
            print(f"Syncing commands to guild {guild_id}")
            await self.tree.sync(guild=my_guild)

        # global sync - takes an hour
        # await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command(
    name="tb-ops-score-report",
    description="TB report on operations scores")
@app_commands.rename(ally_code='ally-code',
                     max_phase='max-phase')
@app_commands.describe(
    ally_code="The player's ally code",
    guild='True to report on the guild, false for the player only (default is False)',
    max_phase='The maximum TB phase to include (default is 6 for all phases)',
    verbose='set to False for a shorter report (default is True)',
)
async def op_score(interaction: discord.Interaction, ally_code: str, guild: bool = False,
                   max_phase: app_commands.Range[int, 1, 6] = 6,
                   verbose: bool = True):
    await interaction.response.defer()
    (title, description) = report_generator.op_score_report(ally_code, guild, max_phase, verbose)
    embed = discord.Embed(title=title, description=description, color=0xd1d4d7)
    await interaction.followup.send(embed=embed)


try:
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")

    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    # handler = None
    client.run(token, log_handler=handler)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
