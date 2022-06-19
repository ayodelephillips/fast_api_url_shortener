from typing import List, Optional
from pydantic import BaseModel


class UrlBase(BaseModel):
    url: str


class UrlCreate(UrlBase):
    """used when saving url to the db. It specifies the long_url, short_code as important variables when saving url to db"""
    long_url: str
    short_code: str


# UrlBase acts as a form of basic template that future classes like UrlCreate can inherit from