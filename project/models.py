from .myapp import db
from flask_login import UserMixin
from sqlalchemy import Sequence

class Users(UserMixin, db.Model): # UserMixin allows server code to check if a user is logged in 
    personid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    wins = db.Column(db.Integer)
    playtime = db.Column(db.Integer)
    def get_id(self):
           return (self.personid)
    
class Questions(db.Model):
    questionid = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    title = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    difficulty = db.Column(db.Integer)
    def get_id(self):
           return (self.questionid)
    
class Games(db.Model):
    gameid = db.Column(db.Integer, primary_key=True) 
    # gamequestions = db.Column(db.Integer)
    # personid = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    broadcast = db.Column(db.Boolean)
    fullresults = db.Column(db.Boolean)
    def get_id(self):
           return (self.gameid)
    
class game_players(db.Model):
    playerid = db.Column(db.String(1000), Sequence('game_players_id_seq'), primary_key=True) # primary keys are required by SQLAlchemy
    # Sequence is used to auto increment the playerid when a new player is added to the table
    gameid = db.Column(db.Integer)
    playername = db.Column(db.String(255))
    #questionsanswered = db.Column(db.Integer)
    score = db.Column(db.Integer)
    def get_id(self):
           return (self.gameid)

class gamequestions(db.Model):
    primkey = db.Column(db.Integer, primary_key=True)
    gameid = db.Column(db.Integer)
    questionid = db.Column(db.Integer)
    personid = db.Column(db.Integer)
    def get_id(self):
           return (self.gameid)