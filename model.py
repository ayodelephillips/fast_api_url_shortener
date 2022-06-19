from sqlalchemy import Column, Integer, String
from db import Base


class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True)
    short_code = Column(String, index=True)
    short_url = Column(String, index=True)
