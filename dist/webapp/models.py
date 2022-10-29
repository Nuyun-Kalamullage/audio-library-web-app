#from webapp.extensions import db
from flask_sqlalchemy import SQLAlchemy
from fastapi_utils.guid_type import GUID
from uuid import uuid4
from webapp import db

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False, unique=True)
  alt_title = db.Column(db.String(200), nullable=True, unique=False)
  cover_img = db.Column(db.String(100), nullable=False, unique=False, default="default_cover.jpg")
  synopsis = db.Column(db.String(1000), nullable=True, unique=False)
  type = db.Column(db.String(50), nullable=False, unique=False)
  status = db.Column(db.String(50), nullable=False, unique=False)
  language = db.Column(db.String(50), nullable=False, unique=False)
  views = db.Column(db.Integer, nullable=False, default=0)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'),nullable=False)

  def __repr__(self):
    return f'{self.title}'

class Chapter(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  order = db.Column(db.Integer, nullable=False, unique=True)
  display_number = db.Column(db.String(10), nullable=False, unique=False)
  audio_url = db.Column(db.String(100), nullable=False, unique=False, default="sample.mp3")
  read_text_url = db.Column(db.String(100), nullable=True, unique=False)
  views = db.Column(db.Integer, nullable=False, default=0)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False)

  def __repr__(self):
    return f'Chapter-{self.display_number}'

class Genre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50), nullable=False, unique=True)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  def __repr__(self):
    return f'{self.title}'

class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), nullable=False, unique=True)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  def __repr__(self):
    return f'{self.name}'