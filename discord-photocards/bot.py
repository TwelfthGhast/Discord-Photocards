import os

import discord

from .commands import get_command_class
from .constants import COMMAND_PREFIX

token = os.getenv("DISCORD_PHOTOCARD_TOKEN")

client = discord.Client()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    elif not message.channel.name in ["bot-commands"]:
        return
    elif not message.content.startswith(COMMAND_PREFIX):
        return

    await message.channel.send(**get_command_class(message).process())


client.run(token)
