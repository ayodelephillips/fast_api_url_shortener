from sqlalchemy.orm import Session

import model
import pydan_schema


def save_url_to_db(db: Session, url: pydan_schema.UrlCreate):
    db_item = model.Url(long_url=url['long_url'], short_code=url['short_code'], short_url=url['short_url'])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_url_by_short_code(db: Session, short_code:str):
    return db.query(model.Url).filter(model.Url.short_code == short_code).first()


def get_long_url_by_short_url(db: Session, short_url:str):
    return db.query(model.Url).filter(model.Url.short_url == short_url).first()