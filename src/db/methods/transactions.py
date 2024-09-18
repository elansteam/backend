from db.client import client


def with_transaction(func):
    async def wrapper(*args, **kwargs):
        try:
            with client.start_session() as session:
                with session.start_transaction():
                    result = func(*args, **kwargs, session=session)
                    return result
        except Exception as e:
            raise e

    return wrapper
