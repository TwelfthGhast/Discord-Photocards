from .base_class import BotCommand
from ..constants import COMMAND_PREFIX
from ..collections import get_collection
from ..db import get_database_handler
from ..images import get_collection_picture
import discord

class ViewBotCommand(BotCommand):
    # Commands should be unique
    _command = "view"
    _help = {"content": '\n'.join([
        f"{COMMAND_PREFIX}{_command} help",
        "",
        "Usage:",
        f"\t\t{COMMAND_PREFIX}{_command} <collection>",
        "\t\t\t\t- Shows your collected cards for <collection>",
        f"\t\t{COMMAND_PREFIX}{_command} <collection> <n>",
        "\t\t\t\t- Shows you the <n>th card in the <collection>",
    ])}

    def __init__(self, message, author_id):
        self.message = message
        self.author_id = author_id

    def process(self):
        message_data = self.message.split()
        if not len(message_data) or len(message_data) > 2:
            return self._help

        # check if collection exists
        collection_name = message_data[0]
        collection = get_collection(collection_name)
        if not collection:
            return {
                "content": f"Collection '{collection_name}' does not exist."
            }
        
        if len(message_data) == 1:
            owned_images = get_database_handler().get_owned_images(self.author_id, collection_name)
            # TODO: render and return collection image
            return {
                "content": f"You have collected {len(owned_images)}/{collection.num_items} cards in '{collection.name}'",
                "files": [discord.File(get_collection_picture(collection, owned_images), filename="collection.jpg")]
            }
        elif len(message_data) == 2:
            collection_name, item_no = message_data
            try:
                item_no = int(item_no)
                # adjust from "user-number" to "array-number"
                item_no -= 1
            except:
                return self._help
            
            if not item_no in range(collection.num_items):
                return {
                    "content": f"Collection '{collection_name}' has {collection.num_items} items. Item {item_no} is invalid."
                }

            owned_images = get_database_handler().get_owned_images(self.author_id, collection_name)
            if item_no in owned_images:
                return {
                    "content": f"Card {item_no + 1} of {collection_name}.",
                    "files": [discord.File(collection.image_paths[item_no], filename=collection.image_paths[item_no].name)]
                }
            else:
                return {
                    "content": f"You do not currently own card {item_no + 1} of {collection_name}.",
                    "files": [discord.File(collection.preview_path, filename=collection.preview_path.name)]
                }

    '''
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
            msg_list = 
            msg_collated = "\n".join(msg_list)
            await message.channel.send(msg_collated)
            return
    '''
