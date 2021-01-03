from typing import List

import discord

from ..collections import get_collection
from ..constants import COMMAND_PREFIX
from ..db import get_database_handler
from ..images import get_collection_picture
from .base_class import BotCommand


class UnlockBotCommand(BotCommand):
    # Commands should be unique
    _command = "unlock"
    _help = {
        "content": "\n".join(
            [
                f"{COMMAND_PREFIX}{_command} help",
                "",
                "Usage:",
                f"\t\t{COMMAND_PREFIX}{_command} <collection> <n> <username>",
                "\t\t\t\t - Unlocks the <n>th item in <collection> for <username>",
                "\t\t\t\t - <username> should be a discord mention",
            ]
        )
    }
    _admin = True

    def __init__(self, message: str, author_id: int, mentions: List[discord.Member]):
        self.message = message
        self.author_id = author_id
        self.mentions = mentions
        self.db_handler = get_database_handler()

    def process(self):
        message_data = self.message.split()
        if len(message_data) != 3:
            return self._help
        if len(self.mentions) != 1:
            return {"content": f"Expected one mention: recieved {len(self.mentions)}"}
        user_id = self.mentions[0].id
        collection_name, img_ids = message_data[:2]
        collection = get_collection(collection_name)
        if collection is None:
            return {"content": f"Collection '{collection_name}' does not exist."}
        img_ids = img_ids.split(",")
        message = []
        for img_id in img_ids:
            try:
                img_id = int(img_id)
                img_id -= 1
            except:
                message.append(f"'{img_id}' is not an integer")
                continue
            if not img_id in range(collection.num_items):
                message.append(
                    f"Collection '{collection_name}' has {collection.num_items} images. Item {img_id} is invalid."
                )
                continue
            self.db_handler.unlock_image(user_id, collection_name, img_id + 1)
        owned_images = self.db_handler.get_owned_images(user_id, collection_name)
        return {
            "content": "\n".join(message),
            "files": [
                discord.File(
                    get_collection_picture(collection, owned_images),
                    filename="collection.jpeg",
                )
            ],
        }
