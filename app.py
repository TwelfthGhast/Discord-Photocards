import os
from functions import cmd_unlock, cmd_tcg, cmd_print_collections
from util import TCGCollection, TCGUser, getTCGUser, getCollection, ImageToByteStream
from PIL import Image, ImageDraw
import discord
import math



client = discord.Client()

COMMAND_ONE = '$tcg'
COMMAND_TWO = '$unlock'
COMMAND_THREE = '$collections'
COMMAND_FOUR = '$help'
ALL_COMMANDS = [COMMAND_ONE, COMMAND_TWO, COMMAND_THREE, COMMAND_FOUR]


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if str(message.channel) != "bot-spam":
        return

    # General TCG menu
    if message.content.startswith(COMMAND_ONE):
        await cmd_tcg(message, COMMAND_ONE)

    # Unlock cards in collection
    if message.content.startswith(COMMAND_TWO):
        await cmd_unlock(message, COMMAND_TWO)

    # List all collections
    if message.content.startswith(COMMAND_THREE):
        await cmd_print_collections(message, COMMAND_THREE)

    # List all commands
    if message.content.startswith(COMMAND_FOUR):
        msg_list = ["Here are all the commands:"]
        for command in ALL_COMMANDS:
            msg_list.append(f"\t\t- {command}")
        msg_collected = "\n".join(msg_list)
        await message.channel.send(msg_collected)
        return

for collection in os.listdir("collections"):
    width = 0
    height = 0
    images = []
    preview = None
    for image in os.listdir(f"collections/{collection}"):
        if image == "dimensions.txt":
            fh = open(f"collections/{collection}/{image}", "r")
            try:
                width = int(fh.readline())
                height = int(fh.readline())
            except Exception as e:
                print(f"Error reading dimensions.txt from collections/{collection}:\t{e}")
                print(f"Skipping collection...")
                break
        elif image == "preview.jpg":
            preview = image
        else:
            images.append(image)
    if width == 0 or height == 0 or len(images) == 0:
        next
    temp_TCG = TCGCollection(collection, images, (width, height), math.ceil(math.sqrt(len(images))), preview)

client.run(token)
