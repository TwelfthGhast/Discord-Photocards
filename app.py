import os
from functions import cmd_unlock, cmd_tcg, cmd_print_collections, cmd_lock
from util import TCGCollection, TCGUser, getTCGUser, getCollection, ImageToByteStream
from PIL import Image, ImageDraw
import discord
import math
import signal
import pickle
import atexit
import threading
from time import sleep
import datetime
token = ""


client = discord.Client()

COMMAND_ONE = '$tcg'
COMMAND_TWO = '$unlock'
COMMAND_THREE = '$collections'
COMMAND_FOUR = '$help'
COMMAND_FIVE = '$lock'
COMMON_CMD = [COMMAND_ONE, COMMAND_THREE, COMMAND_FOUR]
ADMIN_CMD = [COMMAND_TWO, COMMAND_FIVE]

ADMINS = [
    "12Ghast#4326"
]

BACKUP_DIR = "backup"
USER_BACKUP = f"{BACKUP_DIR}/user.p"


def cleanup_function():
    print("Attempting to save users...")
    try:
        pickle_user_file = open(USER_BACKUP, "wb")
        pickle.dump(TCGUser.all_users, pickle_user_file)
        pickle_user_file.close()
        print("Saved users")
    except Exception as err:
        print("An error occurred when saving user database:")
        print(e)


def regular_backup(seconds=60*60*3):
    while True:
        sleep(seconds)
        time = datetime.datetime.now()
        backup_name = f"{BACKUP_DIR}/user-{int(time.timestamp())}.p"
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Saving a backup to {backup_name}")
        pickle_user_file = open(backup_name, "wb")
        pickle.dump(TCGUser.all_users, pickle_user_file)
        pickle_user_file.close()


def read_pickle(filename):
    pickle_msg_file = open(filename, "rb")
    data = pickle.load(pickle_msg_file)
    pickle_msg_file.close()
    return data


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif str(message.channel) != "vcard-game-testing":
        return

    args = message.content.split()
    if args[0] in ADMIN_CMD:
        if str(message.author) not in ADMINS:
            await message.channel.send("You do not have permission to perform this action!")
            return

    # General TCG menu
    if message.content.startswith(COMMAND_ONE):
        await cmd_tcg(message, COMMAND_ONE)
    # Unlock cards in collection
    elif message.content.startswith(COMMAND_TWO):
        await cmd_unlock(message, COMMAND_TWO)
    # List all collections
    elif message.content.startswith(COMMAND_THREE):
        await cmd_print_collections(message, COMMAND_THREE)
    # List all commands
    elif message.content.startswith(COMMAND_FOUR):
        msg_list = ["Here are all the commands:"]
        ALL_COMMANDS = COMMON_CMD
        if str(message.author) in ADMINS:
            ALL_COMMANDS += ADMIN_CMD
        for command in ALL_COMMANDS:
            msg_list.append(f"\t\t- {command}")
        msg_collected = "\n".join(msg_list)
        await message.channel.send(msg_collected)
    # Lock cards in collection
    elif message.content.startswith(COMMAND_FIVE):
        await cmd_lock(message, COMMAND_FIVE)
    return

for collection in os.listdir("collections"):
    width = 0
    height = 0
    images = []
    preview = None
    for image in sorted(os.listdir(f"collections/{collection}")):
        if image == "dimensions.txt":
            fh = open(f"collections/{collection}/{image}", "r")
            try:
                width = int(fh.readline())
                height = int(fh.readline())
            except Exception as e:
                print(
                    f"Error reading dimensions.txt from collections/{collection}:\t{e}")
                print(f"Skipping collection...")
                break
        elif image == "preview.jpg":
            preview = image
        else:
            images.append(image)
    if width == 0 or height == 0 or len(images) == 0:
        next
    temp_TCG = TCGCollection(collection, images, (width, height), math.ceil(
        math.sqrt(len(images))), preview)

print("Creating thread for periodic backups")
x = threading.Thread(target=regular_backup, daemon=True)
x.start()

print("Attempting to import users from file")
if os.path.exists(USER_BACKUP) and os.path.isfile(USER_BACKUP):
    try:
        TCGUser.all_users = read_pickle(USER_BACKUP)
        print(f"Imported users from {USER_BACKUP}")
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
else:
    print(f"Could not find {USER_BACKUP}")
atexit.register(cleanup_function)

client.run(token)
