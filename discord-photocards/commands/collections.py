from ..collections import get_collections
from ..constants import COMMAND_PREFIX
from .base_class import BotCommand


class CollectionsBotCommand(BotCommand):
    # Commands should be unique
    _command = "collections"
    _admin = False

    def __init__(self, message, author_id, mentions):
        # these are useless for collections
        self.message = message
        self.author_id = author_id
        self.mentions = mentions

    def process(self):
        msg = ["Here is a list of all collections"]
        for collection in get_collections():
            msg.append(f"\t-\t{collection}")
        return {"content": "\n".join(msg)}
