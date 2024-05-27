from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


from src.typing.base import Creds, DBAdapater


def get_engine(creds: Creds, adapter: DBAdapater = DBAdapater.postgres) -> Engine:
	return create_engine(creds.to_url(adapter=adapter))
