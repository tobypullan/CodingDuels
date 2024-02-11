from .myapp import db
from flask_login import UserMixin
from sqlalchemy import Sequence

class Users(UserMixin, db.Model):
    personid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    def get_id(self):
           return (self.personid)
    
class Questions(db.Model):
    questionid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    difficulty = db.Column(db.Integer)
    answers = db.Column(db.Integer)
    def get_id(self):
           return (self.questionid)
    
class Games(db.Model):
    gameid = db.Column(db.Integer) 
    gamequestions = db.Column(db.Integer)
    personid = db.Column(db.Integer)
    primkey = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    def get_id(self):
           return (self.gameid)
    
class game_players(db.Model):
    playerid = db.Column(db.String(1000), Sequence('game_players_id_seq'), primary_key=True) # primary keys are required by SQLAlchemy
    gameid = db.Column(db.Integer)
    playername = db.Column(db.String(255))
    questionsanswered = db.Column(db.Integer)
    def get_id(self):
           return (self.gameid)
# class gameids(db.Model):
#     gameid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
#     socketid = db.Column(db.String(1000))
#     def get_id(self):
#            return (self.gameid)