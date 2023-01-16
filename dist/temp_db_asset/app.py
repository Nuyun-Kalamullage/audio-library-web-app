from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_pswd = os.getenv('DB_PSWD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_pswd}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from admin_model import User, Userlevel

book_genres = db.Table("book_genres",
  db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
  db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
)

class Book(db.Model):
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  title = db.Column(db.String(100), nullable=False, unique=True)
  alt_title = db.Column(db.String(200), nullable=True, unique=False)
  cover_img = db.Column(db.String(100), nullable=False, unique=False, server_default="default_cover.jpg")
  synopsis = db.Column(db.String(1000), nullable=True, unique=False)
  status = db.Column(db.String(50), nullable=False, unique=False)
  language = db.Column(db.String(50), nullable=False, unique=False)
  views = db.Column(db.Integer, nullable=False, default=0)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  author_name = db.Column(db.String(200), nullable=False, unique=False)
  is_approved = db.Column(db.Boolean, unique=False, default=0)
  draft_user_email = db.Column(db.String(200), db.ForeignKey(User.email),nullable=False)
  chapters = db.relationship('Chapter', backref="book")
  genres = db.relationship("Genre", secondary=book_genres, back_populates="books")
  users = db.relationship(User, backref="book")

  def __repr__(self):
    return f'{self.title}'

class Genre(db.Model):
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  title = db.Column(db.String(100), nullable=False, unique=True)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  books = db.relationship("Book", secondary=book_genres, back_populates="genres")

  def __repr__(self):
    return f'{self.id}-{self.title}'

class Chapter(db.Model):
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  order = db.Column(db.Integer, nullable=False, unique=True)
  display_number = db.Column(db.String(10), nullable=False, unique=False)
  audio_url = db.Column(db.String(100), nullable=False, unique=False, server_default="sample.mp3")
  is_convert = db.Column(db.Boolean, unique=False, default=0)
  read_text_url = db.Column(db.String(100), nullable=True, unique=False)
  views = db.Column(db.Integer, nullable=False, default=0)
  created = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
  uploaded_by = db.Column(db.String(200), db.ForeignKey(User.email),nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False)
  users = db.relationship(User, backref="chapter")

  def __repr__(self):
    return f'Chapter-{self.display_number}'

  @property
  def elapsed_time(self):
    return (self.updated.strftime("%d/%m/%Y"))

class Library(db.Model):
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False, primary_key=True)
  user_email = db.Column(db.String(200), db.ForeignKey(User.email),nullable=False, primary_key=True)

  def __repr__(self):
    return f'Library-{self.book_id}-{self.user_email}'

class Rating(db.Model):
  book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False, primary_key=True)
  user_email = db.Column(db.String(200), db.ForeignKey(User.email),nullable=False, primary_key=True)
  rate_score = db.Column(db.Integer, nullable=False)
  created_date = db.Column(db.DateTime, server_default=db.func.now())
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

  def __repr__(self):
    return f'Rating-{self.book_id}-{self.user_email}-score{self.rate_score}'

class ReportBook(db.Model):
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  user_email = db.Column(db.String(200), db.ForeignKey(User.email),nullable=False)
  title = db.Column(db.String(100), nullable=False, unique=False)
  subject = db.Column(db.String(1000), nullable=True, unique=False)
  is_read = db.Column(db.Boolean, unique=False, default=0)
  created_date = db.Column(db.DateTime, server_default=db.func.now())

  def __repr__(self):
    return f'Report-{self.id}-{self.title}-{self.user_email}'

class NewsLetterSubscription(db.Model):
    subscription_id = db.Column(db.Integer, autoincrement=True, nullable=False, unique=True, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True, primary_key=True)
    created_date = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'MailID-{self.subscription_id}'


db.drop_all()
db.create_all()

#skeleton data

memberlvl = Userlevel(id=0, title="member")
adminlvl = Userlevel(id=1, title="admin")

db.session.add(memberlvl)
db.session.add(adminlvl)

objects = [
    Genre(title="Action and Adventure"),
    Genre(title="Classics"),
    Genre(title="Graphic Novel"),
    Genre(title="Detective and Mystery"),
    Genre(title="Fantasy"),
    Genre(title="Horror"),
    Genre(title="Literary Fiction"),
    Genre(title="Romance"),
    Genre(title="Women's Fiction"),
    Genre(title="Biographies and Autobiographies"),
    Genre(title="Science Fiction (Sci-Fi)"),
    Genre(title="Short Stories"),
    Genre(title="Suspense and Thrillers"),
    Genre(title="Historical Fiction"),
    Genre(title="Cookbooks"),
    Genre(title="Essays"),
    Genre(title="History"),
    Genre(title="Memoir"),
    Genre(title="Poetry"),
    Genre(title="Self-Help"),
    Genre(title="True Crime")
]
db.session.bulk_save_objects(objects)
db.session.commit()

##### Optional
user1 = User(username="Dulan Pabasara", email="dulan9595531@gmail.com", password="$2b$12$Ay2Ln/FGK5lfD.DSrT3/7uIWUUudC8KFSrB5FSoeVEDafMx/BnTtW")
book1 = Book(
  title='Oliver Twist', 
  alt_title="The Parish Boy's Progress", 
  cover_img="689698d5-ac26-4e76-a97b-a0d7d9cece7a-new_title_cover.png", 
  synopsis="Oliver Twist is a young orphan. His life in the workhouse is lonely and sad. Oliver becomes an apprentice for an undertaker but runs away after he gets into a fight with another apprentice. When Oliver arrives in London, he meets Jack, also known as the Artful Dodger, who offers him a place to stay.", 
  status="Completed", 
  language="English", 
  author_name="Charles Dickens", 
  draft_user_email="dulan9595531@gmail.com",
  is_approved=1)
book2 = Book(
  title='A Tale of Two Cities', 
  alt_title="A Tale of Two Cities (1997)", 
  cover_img="689698d5-ac26-4e76-a97b-a0d7d9cece7a-new_title_cover.png", 
  synopsis="A Tale of Two Cities is a historical novel published in 1859 by Charles Dickens, set in London and Paris before and during the French Revolution.", 
  status="Completed", 
  language="English", 
  author_name="Charles Dickens", 
  draft_user_email="dulan9595531@gmail.com",
  is_approved=1)
book3 = Book(
  title='A Study in Scarlet', 
  alt_title="A Study in Scarlet (1987)", 
  cover_img="689698d5-ac26-4e76-a97b-a0d7d9cece7a-new_title_cover.png", 
  synopsis="A Study in Scarlet is an 1887 detective novel by British writer Arthur Conan Doyle. The story marks the first appearance of Sherlock Holmes and Dr. Watson, who would become the most famous detective duo in literature.", 
  status="Completed", 
  language="English", 
  author_name="Arthur Conan Doyle", 
  draft_user_email="dulan9595531@gmail.com",
  is_approved=1)
genre_obj_classics = db.session.query(Genre).filter_by(id=2).first()
genre_obj_mystery = db.session.query(Genre).filter_by(id=4).first()
book1.genres.append(genre_obj_classics)
book2.genres.append(genre_obj_classics)
book3.genres.append(genre_obj_classics)
book3.genres.append(genre_obj_mystery)
db.session.add(user1)
db.session.commit()
db.session.add(book1)
db.session.add(book2)
db.session.add(book3)
db.session.commit()
######