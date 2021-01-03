from ..constants import ADMINS, COMMAND_PREFIX
from .base_class import BotCommand


class HelpBotCommand(BotCommand):
    # Commands should be unique
    _command = "help"
    _admin = False

    def __init__(self, message, author_id, mentions):
        # these are useless for help command
        self.message = message
        self.author_id = author_id
        self.mentions = mentions

    def process(self):
        msg = ["Here is a list of all available commands"]
        for command_suffix in sorted(self._command_registry):
            if not self._command_is_admin[command_suffix] or self.author_id in ADMINS:
                msg.append(f"\t-\t{COMMAND_PREFIX}{command_suffix}")
        return {"content": "\n".join(msg)}
