import discord
from PIL import Image, ImageDraw
from util import getCollection, TCGCollection, TCGUser, getTCGUser, ImageToByteStream
import math

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
