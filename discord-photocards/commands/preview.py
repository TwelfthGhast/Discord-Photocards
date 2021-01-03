from .base_class import BotCommand
from ..constants import COMMAND_PREFIX
from ..collections import get_collection
from ..db import get_database_handler
from ..images import get_collection_picture
import discord

class PreviewBotCommand(BotCommand):
    # Commands should be unique
    _command = "preview"
    _help = {"content": '\n'.join([
        f"{COMMAND_PREFIX}{_command} help",
        "",
        "Usage:",
        f"\t\t{COMMAND_PREFIX}{_command} <collection>",
        "\t\t\t\t- Shows cards for <collection>",
        f"\t\t{COMMAND_PREFIX}{_command} <collection> <n>",
        "\t\t\t\t- Shows you the <n>th card in the <collection>",
    ])}
    _admin = True

    def __init__(self, message, author_id, mentions):
        self.message = message
        self.author_id = author_id
        self.mentions = mentions

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
            owned_images = list(range(1, get_collection(collection_name).num_items + 1))
            # TODO: render and return collection image
            return {
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
                    "content": f"Collection '{collection_name}' has {collection.num_items} items. Item {item_no + 1} is invalid."
                }

            return {
                "content": f"Card {item_no + 1} of {collection_name}.",
                "files": [discord.File(collection.image_paths[item_no], filename=collection.image_paths[item_no].name)]
            }