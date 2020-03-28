import discord
from PIL import Image, ImageDraw
from util import getCollection, TCGCollection, TCGUser, getTCGUser, ImageToByteStream
import math


async def cmd_tcg(message, COMMAND_NAME):
    username = str(message.author)
    user = getTCGUser(username)
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
        height = math.floor(
            collClass.size / collClass.width) if collClass.size % collClass.width == 0 else math.ceil(collClass.size / collClass.width)
        single_w, single_h = collClass.img_size
        BORDER_SIZE = 20
        dimensions = (width * single_w + (width + 1) * BORDER_SIZE,
                      height * single_h + (height + 1) * BORDER_SIZE)
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
                draw.rectangle([(left_offset, top_offset), (left_offset +
                                                            single_w, top_offset + single_h)], fill=(255, 255, 255))
            else:
                temp_image = Image.open(f"collections/{collClass.name}/{collClass.preview}")
                temp_image = temp_image.resize(
                    (single_w, single_h), Image.ANTIALIAS)
                image.paste(temp_image, (left_offset, top_offset,
                                         left_offset + single_w, top_offset + single_h))
        # Now place images in
        # userClass has numbers from 1 to arraySize, so we will need to subtract 1
        for itemNo in user.collected[collClass.name]:
            itemNo -= 1
            temp_image = Image.open(f"collections/{collClass.name}/{collClass.items[itemNo]}")
            temp_image = temp_image.resize(
                (single_w, single_h), Image.ANTIALIAS)
            # Find position of item
            row = math.floor(itemNo/collClass.width)
            top_offset = row * single_h + BORDER_SIZE * (row + 1)
            col = itemNo % collClass.width
            left_offset = col * single_w + BORDER_SIZE * (col + 1)
            # paste the loaded image onto prepared background
            image.paste(temp_image, (left_offset, top_offset,
                                     left_offset + single_w, top_offset + single_h))
        imgs = [discord.File(ImageToByteStream(
            image), filename="collection.jpeg")]
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
            imgs = [discord.File(f"collections/{collClass.name}/{collClass.items[item-1]}",
                                 filename="collection.jpeg")]
            await message.channel.send(f"Card {item} in '{collClass.name}'", files=imgs)
            return
    else:
        msg_list = [
            f"{COMMAND_NAME} help",
            "",
            "Usage:",
            f"\t\t{COMMAND_NAME} <collection>",
            "\t\t\t\t- Shows your collected cards for <collection>",
            f"\t\t{COMMAND_NAME} <collection> <n>",
            "\t\t\t\t- Shows you the <n>th card in the <collection>",
        ]
        msg_collated = "\n".join(msg_list)
        await message.channel.send(msg_collated)
        return


async def cmd_unlock(message, COMMAND_NAME):
    inputdata = message.content.split()
    len_input = len(inputdata)
    if len_input == 4:
        cmd, coll, item, u_mention = inputdata
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
        try:
            user_mention = message.mentions[0]
        except:
            await message.channel.send(f"You did not mention anyone in the command!")
            return
        for g_member in message.channel.guild.members:
            if g_member == user_mention:
                u_name = str(g_member)
                uClass = getTCGUser(u_name)
                if collClass.name in uClass.collected:
                    if item in uClass.collected[collClass.name]:
                        await message.channel.send(f"{u_name} already owns card {item} of collection '{collClass.name}'!")
                        return
                    uClass.collected[collClass.name].append(item)
                else:
                    uClass.collected[collClass.name] = [item]
                await message.channel.send(f"{message.author.mention} unlocked card number {item} from '{collClass.name}' for  {user_mention.mention}! Congratulations!")
                return
        await message.channel.send(f"{u_mention} was not found in the server.")
    else:
        await message.channel.send(f"{COMMAND_NAME} help\n\nUsage:\n\t\t{COMMAND_NAME} <collection> <n> <username>\
                \n\t\t\t\t - Unlocks the <n>th item in <collection> for <username>\
                \n\t\t\t\t - <username> should be a discord mention")
    return

async def cmd_lock(message, COMMAND_NAME):
    inputdata = message.content.split()
    len_input = len(inputdata)
    if len_input == 4:
        cmd, coll, item, u_mention = inputdata
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
        try:
            user_mention = message.mentions[0]
        except:
            await message.channel.send(f"You did not mention anyone in the command!")
            return
        for g_member in message.channel.guild.members:
            if g_member == user_mention:
                u_name = str(g_member)
                uClass = getTCGUser(u_name)
                if collClass.name in uClass.collected:
                    if item not in uClass.collected[collClass.name]:
                        await message.channel.send(f"{u_name} does not own card {item} of collection '{collClass.name}'!")
                        return
                    uClass.collected[collClass.name].remove(item)
                else:
                    uClass.collected[collClass.name] = []
                await message.channel.send(f"{message.author.mention} removed card number {item} from '{collClass.name}' from  {user_mention.mention} :(")
                return
        await message.channel.send(f"{u_mention} was not found in the server.")
    else:
        await message.channel.send(f"{COMMAND_NAME} help\n\nUsage:\n\t\t{COMMAND_NAME} <collection> <n> <username>\
                \n\t\t\t\t - Locks the <n>th item in <collection> for <username>\
                \n\t\t\t\t - <username> should be a discord mention")
    return


async def cmd_print_collections(message, COMMAND_NAME):
    msg_list = ["Here is a list of all collections:"]
    for collection in TCGCollection.all_collections:
        msg_list.append(f"\t\t- {collection.name}")
    msg_collected = "\n".join(msg_list)
    await message.channel.send(msg_collected)
    return
