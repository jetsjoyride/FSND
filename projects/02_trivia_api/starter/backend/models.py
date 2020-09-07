import os
from flask import Flask
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

PGHOST = 'localhost'
PGDATABASE = 'trivia'
PGUSER = 'postgres'
PGPASSWORD = 'postgres'
database_path = 'postgresql://' + PGUSER + ':' + PGPASSWORD + '@' + PGHOST + ':5432/' + PGDATABASE
# database_name = 'trivia'
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

# Code needed to test directly in python
# app = Flask(__name__)
# db = SQLAlchemy(app)

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    migrate.init_app(app, db)

'''
Question

'''
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(Integer, primary_key=True)
    question = db.Column(String)
    answer = db.Column(String)
    category_id = db.Column(Integer, db.ForeignKey('categories.id'))
    difficulty = db.Column(Integer)

    @hybrid_property
    def category(self):
        return self.categories.id

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }

'''
Category

'''
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(Integer, primary_key=True)
    type = db.Column(String)
    questions = db.relationship('Question', backref='categories', cascade='all, delete')

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
          'id': self.id,
          'type': self.type
        }
