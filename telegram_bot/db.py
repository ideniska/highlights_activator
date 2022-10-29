import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect("telegram.db") as conn:
            kwargs["conn"] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS users")

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            user_email        TEXT NOT NULL
        )
    """
    )

    conn.commit()


@ensure_connection
def add_user_email(conn, user_id: int, email: str):
    c = conn.cursor()
    c.execute("INSERT INTO users (user_id, user_email) VALUES (?, ?)", (user_id, email))
    conn.commit()


@ensure_connection
def get_user_email(conn, user_id: int, limit: int):
    c = conn.cursor()
    c.execute(
        "SELECT id, user_email FROM users WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, limit),
    )
    return c.fetchall()
