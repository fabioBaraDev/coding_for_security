import psycopg2
import psycopg2.extras
from app.config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def execute_query(sql, params=None, fetch=True):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            if fetch:
                result = cur.fetchall()
            else:
                result = None
            conn.commit()
            return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_returning(sql, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            result = cur.fetchone()
            conn.commit()
            return result
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
