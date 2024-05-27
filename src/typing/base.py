from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.engine import URL


class DBAdapater(Enum):
	postgres = "postgresql+psycopg2"
	sqlite = "sqlite"


class Creds(BaseModel):
	username: str
	password: str
	host: str
	port: int
	database: Optional[str]

	def to_url(self, adapter: DBAdapater = DBAdapater.postgres) -> URL:
		return URL(
			adapter.value,
			**self.model_dump(),
			query={"sslmode": "disable"},
		)
