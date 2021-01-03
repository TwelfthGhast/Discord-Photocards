import pathlib
import sqlite3

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
        cursor = conn.execute(
            "SELECT photo_id FROM users WHERE photo_group = ? AND userid = ?",
            (collection_name, user_id),
        )
        rows = [x[0] for x in cursor.fetchall()]
        conn.close()
        return rows

    def unlock_image(self, user_id, collection_name, photo_id):
        conn = self._get_conn()
        cursor = conn.execute(
            "INSERT INTO users(userid, photo_group, photo_id) VALUES (?, ?, ?)",
            (user_id, collection_name, photo_id),
        )
        conn.commit()
        conn.close()

    def lock_image(self, user_id, collection_name, photo_id):
        conn = self._get_conn()
        cursor = conn.execute(
            "DELETE FROM users WHERE userid = ? AND photo_group = ? AND photo_id = ?",
            (user_id, collection_name, photo_id),
        )
        conn.commit()
        conn.close()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)


db_handler = Database(DB_NAME)


def get_database_handler():
    return db_handler
