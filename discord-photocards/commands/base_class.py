import abc
import discord
from ..constants import COMMAND_PREFIX
from typing import List

def _get_message_details(message: discord.Message):
    author_id = message.author.id
    try:
        command, rest_of_message = message.content.split(maxsplit=1)
    except ValueError:
        command = message.content.strip()
        rest_of_message = ""
    assert command.startswith(COMMAND_PREFIX)
    command_suffix = command[len(COMMAND_PREFIX):]
    return command_suffix, rest_of_message, author_id, message.mentions


def get_command_class(message: discord.Message):
    return BotCommand().factory(
        *_get_message_details(message)
    )


class BotCommand(abc.ABC):
    _command_registry = {}
    
    @classmethod
    def __init_subclass__(self, **kwargs):
        """Hook into classes that inherit this abstract class and add them to dictionary"""
        super().__init_subclass__(**kwargs)
        self._command_registry[self._command] = self
    
    def factory(self, command_suffix: str, rest_of_message: str, author_id: int, mentions: List[discord.Member]):
        if command_suffix in self._command_registry:
            return self._command_registry[command_suffix](rest_of_message, author_id, mentions)
        else:
            return self._command_registry["help"]("", None)
    
    def process(self):
        raise NotImplementedError
