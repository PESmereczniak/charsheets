from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#pylint: disable=no-member

app = Flask(__name__)
app.config['DEBUG'] = True
#NEEDS CORRECT ADDRESS AND NEW DB!!!
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:rehcr1943@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '123456abcdef'

class char_abilityScores(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.Integer(2))
    dexterity = db.Column(db.Integer(2))
    constitution = db.Column(db.Integer(2))
    intelligence = db.Column(db.Integer(2))
    wisdom = db.Column(db.Integer(2))
    charisma = db.Column(db.Integer(2))

    #MUST DEFINE RELATIONSHIPS WITH OTHER TABLES
    user = db.relationship('User')

    # def __init__(self, blog_title, blog_text, owner):
    #     self.blog_title = blog_title
    #     self.blog_text = blog_text
    #     self.owner = owner

class char_race(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class char_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class char_background(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class char_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    # def __init__(self, email, password):
    #     self.email = email
    #     self.password = password