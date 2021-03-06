from loguru import logger
from asyncpg.connection import Connection
from asyncpg.exceptions import UndefinedColumnError, UndefinedObjectError,\
    UndefinedTableError, UndefinedParameterError, AmbiguousAliasError,\
    WrongObjectTypeError
from asyncpg import Record
from contextvars import ContextVar
from typing import List


_trx_id_ctx_var: ContextVar[str] = ContextVar('trx_id', default=None)


def get_trx_id() -> str:
    return _trx_id_ctx_var.get()


async def query_and_log(
        connection: Connection, query: str, *args) -> List[Record]:

    results = None
    try:
        results = await connection.fetch(query, *args)
    except (
            ValueError,
            UndefinedColumnError,
            UndefinedObjectError,
            UndefinedParameterError,
            UndefinedTableError,
            AmbiguousAliasError,
            WrongObjectTypeError):
        logger.opt(exception=True).error(
            'Found error on query result, check used query: \n{}', query)
    except Exception:
        logger.opt(exception=True).error('Could not get database pool')
    return results


async def insert_and_log(
        connection: Connection, query: str, *args) -> None:

    try:
        await connection.execute(query, *args)
    except (
            ValueError,
            UndefinedColumnError,
            UndefinedObjectError,
            UndefinedParameterError,
            UndefinedTableError,
            AmbiguousAliasError,
            WrongObjectTypeError):
        logger.opt(exception=True).error(
            'Found error on insert query, check used query: \n{}', query)
    except Exception:
        logger.opt(exception=True).error('Could not get database pool')
