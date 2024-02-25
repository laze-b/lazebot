import logging
import os

import discord
from discord import app_commands
from dotenv import load_dotenv

import report_generator
from lazebot.ai import AI
from lazebot.exceptions import *


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        guild_ids = os.getenv("GUILD_IDS")
        if guild_ids:
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


@client.event
async def on_message(message):
    if ai and not message.author.bot and client.user.mentioned_in(message):
        print(f"calling ai.reply_with_humor({client.user.id}, {message.author.id}, {message.content})")
        try:
            response = ai.reply_with_humor(client.user.id, message.author.id, message.content)
            print(f"response={response}")
        except Exception as ex:
            response = "Something went wrong in my circuits. Please try again."
            print(f"Unexpected error with inputs message={message}", ex)

        await message.channel.send(response)


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
    try:
        await interaction.response.defer()
        ally_code = __sanitize_ally_code(ally_code)
        (title, description) = report_generator.op_score_report(ally_code, guild, max_phase, verbose)
        embed = discord.Embed(title=title, description=description, color=0xd1d4d7)
        await interaction.followup.send(embed=embed)
    except PlayerNotFoundException:
        print(f"Player not found for ally_code={ally_code}")
        await interaction.followup.send("Those records are missing from the jedi archives. Please try another another.")
    except Exception as ex:
        print(
            f"Unexpected error with inputs ally_code={ally_code}, guild={guild}, max_phase={max_phase}, verbose={verbose}",
            ex)
        await interaction.followup.send("Something went wrong in my circuits. Please try again.")


def __sanitize_ally_code(ally_code: str):
    ally_code = ally_code.replace("-", "")
    if len(ally_code) != 9:
        raise PlayerNotFoundException
    return ally_code


try:
    load_dotenv()

    # logging setup
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    # handler = None

    # create AI
    gemini_api_key = os.getenv("GEMINI_API_KEY") or ""
    if not gemini_api_key == "":
        ai = AI(gemini_api_key)

    discord_token = os.getenv("DISCORD_TOKEN") or ""
    if discord_token == "":
        raise Exception("Please include a valid DISCORD_TOKEN in the environment.")
    client.run(discord_token, log_handler=handler)
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
