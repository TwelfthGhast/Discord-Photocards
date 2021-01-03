import discord
from .constants import COMMAND_PREFIX
from .commands import get_command_class
token = "NTY0NzUyMzEzMTQzNzg3NTMx.XKsclA.6bom3D1uZfkNGUDtSYP-_0PXZUI"

client = discord.Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        print("client user")
        return
    elif message.channel.name != "12ghast-vcard":
        return
    elif not message.content.startswith(COMMAND_PREFIX):
        print(message.content)
        return
    
    await message.channel.send(**get_command_class(message).process())

client.run(token)