CREATE TABLE IF NOT EXISTS users(
    userid INTEGER NOT NULL,
    photo_group TEXT NOT NULL,
    photo_id INTEGER NOT NULL,
    UNIQUE(userid, photo_group, photo_id) ON CONFLICT IGNORE
);