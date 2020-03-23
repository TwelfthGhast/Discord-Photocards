token = ""

import discord
from PIL import Image, ImageDraw
import io
import math

client = discord.Client()

class TCGUser:
    all_users = []
    def __init__(self, name):
        self.collected = {}
        self.name = name
        TCGUser.all_users.append(self)

class TCGCollection:
    all_collections = []
    def __init__(self, collection_name, items, img_size, width, preview=None):
        self.width = width
        self.name = collection_name
        self.img_size = img_size
        self.size = len(items)
        self.items = []
        self.preview = preview
        for i in items:
            self.items.append(i)
        TCGCollection.all_collections.append(self)


def getTCGUser(name):
    for user in TCGUser.all_users:
        if user.name == name:
            return user
    new_user = TCGUser(name)
    return new_user

def getCollection(collection_name):
    for collection in TCGCollection.all_collections:
        if collection.name == collection_name:
            return collection
    return None

# https://stackoverflow.com/questions/60006794/send-image-from-memory
def ImageToByteStream(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='JPEG')
    imgByteArr.seek(0)
    return imgByteArr

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

    username = str(message.author)
    user = getTCGUser(username)

    # General TCG menu
    if message.content.startswith(COMMAND_ONE):
        inputdata = message.content.split()
        len_input = len(inputdata)
        if len_input == 2:
            cmd, coll = inputdata
            collClass = getCollection(coll)
            if not collClass:
                await message.channel.send(f"The collection '{coll}' does not exist!")
                return

            if collClass.name not in user.collected:
                user.collected[collClass.name] = []
            len_collected = len(user.collected[collClass.name])
            # Create base canvas for returned picture
            width = collClass.width if collClass.width < collClass.size else collClass.size
            height = math.floor(collClass.size / collClass.width) if collClass.size % collClass.width == 0 else math.ceil(collClass.size / collClass.width)
            single_w, single_h = collClass.img_size
            BORDER_SIZE = 20
            dimensions = (width * single_w + (width + 1) * BORDER_SIZE, height * single_h + (height + 1) * BORDER_SIZE)
            image = Image.new('RGB', dimensions, (221, 204, 255))
            # Draw on rectangles where images will be placed
            draw = ImageDraw.Draw(image)
            for i in range(0, collClass.size):
                # all positions are offset from top left corner of rectangle
                row = math.floor(i/collClass.width)
                top_offset = row * single_h + BORDER_SIZE * (row + 1)
                col = i % collClass.width
                left_offset = col * single_w + BORDER_SIZE * (col + 1)
                if not collClass.preview:
                    draw.rectangle([(left_offset, top_offset), (left_offset + single_w, top_offset + single_h)], fill=(255,255,255))
                else:
                    temp_image = Image.open(collClass.preview)
                    image.paste(temp_image, (left_offset, top_offset, left_offset + single_w, top_offset + single_h))
            # Now place images in
            # userClass has numbers from 1 to arraySize, so we will need to subtract 1
            for itemNo in user.collected[collClass.name]:
                itemNo -= 1
                temp_image = Image.open(collClass.items[itemNo])
                # Find position of item
                row = math.floor(itemNo/collClass.width)
                top_offset = row * single_h + BORDER_SIZE * (row + 1)
                col = itemNo % collClass.width
                left_offset = col * single_w + BORDER_SIZE * (col + 1)
                # paste the loaded image onto prepared background
                image.paste(temp_image, (left_offset, top_offset, left_offset + single_w, top_offset + single_h))
            imgs = [ discord.File(ImageToByteStream(image), filename="collection.jpeg") ]
            await message.channel.send(f"You have collected {len_collected}/{collClass.size} cards in '{collClass.name}'", files=imgs)
            return
        elif len_input == 3:
            cmd, coll, item = inputdata
            collClass = getCollection(coll)
            if not collClass:
                await message.channel.send(f"The collection '{coll}' does not exist!")
                return
            try:
                item = int(item)
            except:
                await message.channel.send(f"'{item}' is not a valid item number!")
                return
            if item > collClass.size:
                await message.channel.send(f"The collection '{coll}' has {collClass.size} items, but you wanted number {item}!")
                return
            if item < 0:
                await message.channel.send(f"'{item}' is not a valid item number!")
                return
            if collClass.name not in user.collected or item not in user.collected[collClass.name]:
                await message.channel.send(f"You do not own card number {item} in '{collClass.name}'!")
                return
            else:
                imgs = [ discord.File(collClass.items[item - 1], filename="collection.jpeg") ]
                await message.channel.send(f"Card {item} in '{collClass.name}'", files=imgs)
                return

            

            user = getTCGUser(username)
        else:
            msg_list = [
                f"{COMMAND_ONE} help",
                "",
                "Usage:",
                f"\t\t{COMMAND_ONE} <collection>",
                "\t\t\t\t- Shows your collected cards for <collection>",
                f"\t\t{COMMAND_ONE} <collection> <n>",
                "\t\t\t\t- Shows you the <n>th card in the <collection>",
            ]
            msg_collated = "\n".join(msg_list)
            await message.channel.send(msg_collated)
            return
    
    # Unlock cards in collection
    if message.content.startswith(COMMAND_TWO):
        inputdata = message.content.split()
        len_input = len(inputdata)
        if len_input == 4:
            cmd, coll, item, u_name = inputdata
            collClass = getCollection(coll)
            if not collClass:
                await message.channel.send(f"The collection '{coll}' does not exist!")
                return
            try:
                item = int(item)
            except:
                await message.channel.send(f"'{item}' is not a valid item number!")
                return
            if item > collClass.size:
                await message.channel.send(f"The collection '{coll}' has {collClass.size} items, but you wanted number {item}!")
                return
            if item < 0:
                await message.channel.send(f"'{item}' is not a valid item number!")
                return
            for g_member in message.channel.guild.members:
                g_uname = str(g_member)
                if g_uname == u_name:
                    uClass = getTCGUser(u_name)
                    if collClass.name in uClass.collected:
                        if item in uClass.collected[collClass.name]:
                            await message.channel.send(f"{u_name} already owns card {item} of collection '{collClass.name}'!")
                            return
                        uClass.collected[collClass.name].append(item)
                    else:
                        uClass.collected[collClass.name] = [item]
                    await message.channel.send(f"{u_name} now owns card {item} of collection '{collClass.name}'! Congratulations!")
                    return
            await message.channel.send(f"{u_name} was not found in the server.")
        else:
            await message.channel.send(f"{COMMAND_TWO} help\n\nUsage:\n\t\t{COMMAND_TWO} <collection> <n> <username>\
                \n\t\t\t\t - Unlocks the <n>th item in <collection> for <username>\
                \n\t\t\t\t - <username> should be in format NAME#0000")
        return

    # List all collections
    if message.content.startswith(COMMAND_THREE):
        msg_list = ["Here is a list of all collections:"]
        for collection in TCGCollection.all_collections:
            msg_list.append(f"\t\t- {collection.name}")
        msg_collected = "\n".join(msg_list)
        await message.channel.send(msg_collected)
        return

    # List all commands
    if message.content.startswith(COMMAND_FOUR):
        msg_list = ["Here are all the commands:"]
        for command in ALL_COMMANDS:
            msg_list.append(f"\t\t- {command}")
        msg_collected = "\n".join(msg_list)
        await message.channel.send(msg_collected)
        return
        

    
    #await message.channel.send(f"{message.author.mention} - You are '{message.author.name}#{message.author.discriminator}'")

test = TCGCollection("test", ["test_angry.jpg", "test_girl.jpg", "test_happy.jpg", "test_pacman.jpg"], (350, 600), 3, "test_preview.jpg")
client.run(token)

