# coding: utf-8
from sqlalchemy import (
    CHAR,
    TIMESTAMP,
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    Index,
    Integer,
    String,
    Table,
    Text,
    Time,
    text,
)
from sqlalchemy.dialects.mysql import (
    BIGINT,
    CHAR,
    ENUM,
    INTEGER,
    LONGTEXT,
    MEDIUMTEXT,
    TEXT,
    TINYINT,
    VARCHAR,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Users(Base):
    id = Column(BIGINT, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(15), default=None)
    email = Column(String(320), default="")
