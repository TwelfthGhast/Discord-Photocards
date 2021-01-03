import sqlite3
from ..constants import DB_NAME

class Database:
    def __init__(self, db_name: str):
        self.db = sqlite3.connect(db_name)

db_handler = Database(DB_NAME)

def get_database_handler():
    return db_handler
