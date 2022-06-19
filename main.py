from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse
import os
import model
import pydan_schema
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import validators
import pyshorteners

from utility import save_url_to_db, get_url_by_short_code, get_long_url_by_short_url

model.Base.metadata.create_all(bind=engine)

type_tiny = pyshorteners.Shortener()
tiny_home_url = 'https://tinyurl.com/'

localhost_url = "http://127.0.0.1:8000"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


base_url = 'smaller_url_'


description = """
    Sam's app lets you do two main things
    - accept a url  via the shorten_url endpoint and return its shortened form
    - accept a short url and redirect the caller to the long url
"""

app = FastAPI(
    title='UrlShortener',
    description=description
)


@app.post("/shorten_url/")
def return_shortened_url(url: pydan_schema.UrlBase, db: Session = Depends(get_db)):
    long_url = dict(url)['url'] # url is received as a pydanschema object
    short_code = type_tiny.tinyurl.short(long_url).replace(tiny_home_url, "") # we only need the 7 letter unique code
    short_url = f"{base_url}{short_code}" # the resultant short url which is stored in the db

    # check if short url exists
    short_url_exists = get_url_by_short_code(db=db, short_code=short_code)

    # validate the long url
    if not validators.url(long_url):
        raise HTTPException(status_code=400, detail="The url is invalid") # 400 indicates bad request, client error

    # return the short url if it has already been created before; otherwise, save it to the db
    if short_url_exists is None:
        try:
            db_item = save_url_to_db(db=db, url={'long_url': long_url, 'short_code':short_code, 'short_url':short_url})
            return {"message": "short url generated successfully", "short_url": db_item.short_url}
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"An error occurred while saving to the db. Error is {err}")
    else:
        return {"message": "The url already exists", "short_url":short_url_exists.short_url}


@app.get("/{short_url}")
def redirect_short_url(short_url: str, db: Session = Depends(get_db)):
    # check if short url exists
    short_url_exists = get_long_url_by_short_url(db=db, short_url=short_url)
    if short_url_exists is None:
        raise HTTPException(status_code=404, detail="Short url does not exist")
    response = RedirectResponse(url=short_url_exists.long_url)
    return response
