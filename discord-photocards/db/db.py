import sqlite3
import pathlib
from ..constants import DB_NAME

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name

        conn = self._get_conn()
        schema_path = pathlib.Path(__file__).parent.absolute() / "schema.sql"
        with open(schema_path, "r") as schema:
            conn.executescript(schema.read())
        conn.commit()
        conn.close()
    
    def get_owned_images(self, user_id, collection_name):
        conn = self._get_conn()
        cursor = conn.execute("SELECT photo_id FROM users WHERE photo_group = ?", (collection_name,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

db_handler = Database(DB_NAME)

def get_database_handler():
    return db_handler
