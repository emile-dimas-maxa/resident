import os

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base(metadata=MetaData(schema="SCHEMA"))
Base = declarative_base()
metadata = Base.metadata
