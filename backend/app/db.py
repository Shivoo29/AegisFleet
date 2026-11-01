"""DB layer (M2). psycopg 3 + plain SQL, no ORM."""
import os
from contextlib import contextmanager

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import get_settings

_pool: ConnectionPool | None = None


def _pool_get() -> ConnectionPool:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = ConnectionPool(
            conninfo=settings.database_url,
            min_size=1,
            max_size=10,
            open=True,
            kwargs={"row_factory": dict_row},
        )
    return _pool


@contextmanager
def conn():
    """Yield a connection with dict_row rows."""
    pool = _pool_get()
    with pool.connection() as c:
        yield c


def init_schema() -> None:
    """Execute schema.sql. Fails loudly if DB is down."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "schema.sql")
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    with conn() as c:
        with c.cursor() as cur:
            cur.execute(sql)
        c.commit()