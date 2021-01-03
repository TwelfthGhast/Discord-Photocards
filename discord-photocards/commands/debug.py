from ..constants import ADMINS, COMMAND_PREFIX
from .base_class import BotCommand
from ..db import get_database_handler
from ..collections import get_collections

class DebugBotCommand(BotCommand):
    # Commands should be unique
    _command = "debug"
    _admin = True

    def __init__(self, message, author_id, mentions):
        # these are useless for help command
        self.message = message
        self.author_id = author_id
        self.mentions = mentions
        self.db_handler = get_database_handler()

    def process(self):
        message = []
        for mention in self.mentions:
            user_id = mention.id
            user_name = mention.display_name
            for collection in get_collections():
                owned = self.db_handler.get_owned_images(user_id, collection)
                message.append(f"{user_name} ({user_id}) [{collection}]: {owned}")
        return {
            "content": '\n'.join(message)
        }

