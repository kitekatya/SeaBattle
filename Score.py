import psycopg2
from psycopg2.extras import RealDictCursor
from config import host, user, password, db_name, port


def create_table():
    with psycopg2.connect(host=host, user=user, password=password,
                          database=db_name, port=port) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"CREATE TABLE scores ( player_name VARCHAR(255) UNIQUE NOT NULL, score INT );")
            conn.commit()


def get_scores():
    with psycopg2.connect(host=host, user=user, password=password,
                          database=db_name, port=port) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SELECT player_name, score FROM scores"
                            f" ORDER BY score DESC LIMIT 10;")
            result = cur.fetchall()
    return result


def insert_score(player_name, score):
    with psycopg2.connect(host=host, user=user, password=password,
                          database=db_name, port=port) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"SELECT score FROM scores WHERE player_name = "
                        f"'{player_name}';")
            prev_score = cur.fetchone()
            if prev_score is not None:
                score += prev_score[0]
                cur.execute(f"UPDATE scores SET score = '{score}' WHERE "
                            f"player_name = '{player_name}';")
            else:
                cur.execute(f"INSERT INTO scores (player_name, score) VALUES ("
                            f"'{player_name}', {score});")
