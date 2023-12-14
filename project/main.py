from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import Questions, Games, game_players
#from sqlalchemy import update, func
from random import randint
import requests
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/create')
@login_required
def create():
    question = Questions.query.all()
    global titles
    titles = []
    global gameid
    gameid = randint(0, 1000000000)
    for title in question:
        titles.append(title.title)
    return render_template('create.html', titles=titles)

@main.route('/create', methods=['POST'])
@login_required
def create_post():
    questionTitle = request.form.get('questionTitle')
    questionid = Questions.query.filter_by(title=questionTitle).first()
    # newGameQuestion = Games(gameid=gameid, gamequestions=questionid.questionid)
    # db.session.add(newGameQuestion)
    # db.session.commit()
    return render_template('create.html', title = questionid.title, description = questionid.description, difficulty = questionid.difficulty, titles = titles)

@main.route('/select_question', methods=['POST'])
@login_required
def select_question():
    questionTitle = request.form.get('questionTitle')
    questionid = Questions.query.filter_by(title=questionTitle).first()
    newGameQuestion = Games(gameid=gameid, gamequestions=questionid.questionid, personid=current_user.personid)
    db.session.add(newGameQuestion)
    db.session.commit()
    return render_template('create.html', title = questionid.title, description = questionid.description, difficulty = questionid.difficulty, titles = titles)

@main.route('/start_game', methods=['POST'])
@login_required
def start_game():
    return redirect('/game/' + str(gameid))

@main.route('/game/<gameid>')
@login_required
def game(gameid):
    questions = Games.query.filter_by(gameid=gameid).all()
    questionTitles = []
    for question in questions:
        print(question.gamequestions)
        questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
    return render_template('game.html', questions=questionTitles, gameid=gameid)

@main.route('/game/<gameid>', methods=['POST'])
@login_required
def game_post(gameid):
    playerNames = game_players.query.filter_by(gameid=gameid).all()
    playerNameList = []
    for player in playerNames:
        playerNameList.append(player.playername)
    print(playerNameList)
    questions = Games.query.filter_by(gameid=gameid).all()
    questionTitles = []
    for question in questions:
        questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
    return render_template('game.html', playerNames=playerNameList, questions=questionTitles, gameid=gameid)

@main.route('/game/<gameid>/join')
def join_game(gameid):
    return render_template('join.html', gameid=gameid)

@main.route('/game/<gameid>/join', methods=['POST'])
def join_game_post(gameid):
    name = request.form.get('playername')
    print(name)
    print("the name ^")
    newPlayer = game_players(gameid=gameid, playername=name)
    db.session.add(newPlayer)
    db.session.commit()
    return redirect('/game/' + str(gameid) + '/waiting_room/' + str(newPlayer.playerid))

@main.route('/game/<gameid>/waiting_room/<playerid>')
def waiting_room(gameid, playerid):
    return render_template('waiting_room.html', gameid=gameid, playerid=playerid)

@main.route('/game/<gameid>/waiting_room/<playerid>', methods=['POST'])
def waiting_room_post(gameid, playerid):
    try:
        if gameStarted == True:
            return redirect('/game/' + str(gameid) + '/competition/' + str(playerid))
        else:
            return render_template('waiting_room.html', gameid=gameid, playerid=playerid, waitWarning="Please wait for the host to start the game")
    except:
        return render_template('waiting_room.html', gameid=gameid, playerid=playerid, waitWarning="Please wait for the host to start the game")

@main.route('/game/<gameid>/compeition', methods=['POST'])
def competition(gameid):
    global gameStarted
    gameStarted = True
    return redirect('/game/' + str(gameid) + '/competition/leaderboard')

@main.route('/game/<gameid>/competition/<playerid>', methods=['POST', 'GET'])
def compeition_player(gameid, playerid):
    questions = Games.query.filter_by(gameid=gameid).all()
    questionTitles = []
    for question in questions:
        questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
    return render_template('competition.html', questions=questionTitles, gameid=gameid, playerid=playerid)

@main.route('/game/<gameid>/competition/leaderboard')
@login_required
def leaderboard(gameid):
    return render_template('hostGamePage.html', gameid=gameid)
# @main.route('/<questionid>')
# @login_required
# def question(questionid):
#     question = Questions.query.filter_by(questionid=questionid).first()
#     return render_template('question.html', title=question.title, description=question.description, difficulty=question.difficulty, questionid=questionid)

# @main.route('/<questionid>', methods=['POST'])
# @login_required
# def addToQuestions(questionid, gameid):
#     game = Games.query.filter_by(gameid=gameid).first()
#     if game.gameid == None:
#         gameQuestions = []
#         gameQuestions.append(questionid)
#         new_game = Games(gameQuestions=gameQuestions)
#         db.session.add(new_game)
#         db.session.commit()
#     else:
#         update(Games).where((Games.gameid == gameid)).values(gameQuestions=func.array_append(questionid))
    