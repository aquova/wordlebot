import sqlite3
from config import DATABASE_PATH
from typing import Optional

def init():
    sql = sqlite3.connect(DATABASE_PATH)
    sql.execute("CREATE TABLE IF NOT EXISTS scores (uid INT PRIMARY KEY, total INT, one INT, two INT, three INT, four INT, five INT, six INT)")
    sql.commit()
    sql.close()

def add_score(uid: int, n: int, victory: bool):
    scores = get_scores(uid)
    if not scores:
        scores = [uid, 1, 0, 0, 0, 0, 0, 0]
    scores[1] += 1
    if victory:
        scores[n + 1] += 1

    sql = sqlite3.connect(DATABASE_PATH)
    sql.execute("INSERT OR REPLACE INTO scores (uid, total, one, two, three, four, five, six) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", scores)
    sql.commit()
    sql.close()

def get_scores(uid: int) -> Optional[list[int]]:
    sql = sqlite3.connect(DATABASE_PATH)
    query = sql.execute("SELECT * FROM scores WHERE uid=?", [uid]).fetchone()
    sql.close()
    if query:
        return list(query)
    else:
        return None

