from .base_class import BotCommand
from ..constants import COMMAND_PREFIX

class HelpBotCommand(BotCommand):
    # Commands should be unique
    _command = "help"

    def __init__(self, message, author_id):
        # these are useless for help command
        self.message = message
        self.author_id = author_id
        self.mentions = mentions

    def process(self):
        msg = ["Here is a list of all available commands"]
        for command_suffix in self._command_registry:
            msg.append(f"\t-\t{COMMAND_PREFIX}{command_suffix}")
        return {
            "content": '\n'.join(msg)
        }