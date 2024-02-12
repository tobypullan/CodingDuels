from flask import Blueprint, render_template, request, redirect, jsonify, current_app as app
from flask_login import login_required, current_user
from .myapp import db
from .models import Questions, Games, game_players
#from sqlalchemy import update, func
from random import randint
import requests
from flask_socketio import SocketIO, join_room
from .myapp import socketio


main = Blueprint('main', __name__)
rooms = {}
waitingrooms = {}
leaderboardrooms = {}


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
    # gameid = randint(0, 1000000000)
    # session["gameid"] = gameid
    # db.session.add(gameids(gameid=gameid))
    # db.session.commit()
    questionData = Questions.query.all()
    return render_template('create.html', questionData=questionData)

# @socketio.on("myGameid")
# def handle_myGameid(data):


@socketio.on("create game")
def handle_create_game():
    gameid = randint(0, 1000000000)
    join_room(gameid)
    rooms[gameid] = request.sid
    #db.session.query(gameids).filter(gameids.gameid == gameid).update({'socketid': request.sid})
    print(rooms)
    socketio.emit("game created", {"gameid": gameid}, to=request.sid)

@socketio.on("join game")
def handle_join_game(data):
    gameid = data["gameid"]
    join_room(gameid)
    socketio.emit("game joined", {"success": True}, to=request.sid)
    print("player joined room")


@socketio.on("select question")
def handle_select_question(data):
    #print(f"session in select question: {session}")
    print(rooms)
    questionid = Questions.query.filter_by(title=data["title"]).first()
    newGameQuestion = Games(gameid=data["gameid"], gamequestions=questionid.questionid, personid=current_user.personid)
    db.session.add(newGameQuestion)
    db.session.commit()
    socketio.emit("question selected", {"title": questionid.title, "description": questionid.description, "difficulty": questionid.difficulty}, room=data["gameid"])

@socketio.on("remove question")
def handle_remove_question(questionTitle):
    questionid = Questions.query.filter_by(title=questionTitle["title"]).first()
    db.session.query(Games).filter(Games.gamequestions == questionid.questionid).delete()
    db.session.commit()
    socketio.emit("question removed", {"title": questionid.title})

# @socketio.on("start game")
# def handle_start_game():
#     socketio.emit("game started")

# @main.route('/create')
# @login_required
# def create():
#     question = Questions.query.all()
#     global titles
#     titles = []
#     global gameid
#     gameid = randint(0, 1000000000)
#     for title in question:
#         titles.append(title.title)
#     return render_template('create.html', titles=titles)

# @main.route('/create', methods=['POST'])
# @login_required
# def create_post():
#     questionTitle = request.form.get('questionTitle')
#     questionid = Questions.query.filter_by(title=questionTitle).first()
#     # newGameQuestion = Games(gameid=gameid, gamequestions=questionid.questionid)
#     # db.session.add(newGameQuestion)
#     # db.session.commit()
#     return render_template('create.html', title = questionid.title, description = questionid.description, difficulty = questionid.difficulty, titles = titles)

# @main.route('/select_question', methods=['POST'])
# @login_required
# def select_question():
#     questionTitle = request.form.get('questionTitle')
#     questionid = Questions.query.filter_by(title=questionTitle).first()
#     newGameQuestion = Games(gameid=gameid, gamequestions=questionid.questionid, personid=current_user.personid)
#     db.session.add(newGameQuestion)
#     db.session.commit()
#     return render_template('create.html', title = questionid.title, description = questionid.description, difficulty = questionid.difficulty, titles = titles)

@main.route('/start_game', methods=['POST'])
@login_required
def start_game():
    gameid = request.form.get('gameid')
    print(f"start game gameid: {gameid}")
    #print("Before redirect:", session)
    redirect_url = '/game/' + str(gameid)
    #print("After redirect:", session)
    return redirect(redirect_url)

@main.route('/game/<gameid>')
@login_required
def game(gameid):
    questions = Games.query.filter_by(gameid=gameid).all()
    questionTitles = []
    for question in questions:
        questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
    return render_template('game.html', questions=questionTitles, gameid=gameid)

# @socketio.on("new player")
# def handle_start_game(player):
#     print("player name: " + player["name"])
#     socketio.emit("player joined", player["name"])


# @main.route('/game/<gameid>', methods=['POST'])
# @login_required
# def game_post(gameid):
#     playerNames = game_players.query.filter_by(gameid=gameid).all()
#     playerNameList = []
#     for player in playerNames:
#         playerNameList.append(player.playername)
#     questions = Games.query.filter_by(gameid=gameid).all()
#     questionTitles = []
#     for question in questions:
#         questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
#     return render_template('game.html', playerNames=playerNameList, questions=questionTitles, gameid=gameid)

@main.route('/game/<gameid>/join')
def join_game(gameid):
    return render_template('join.html', gameid=gameid)


# @socketio.on('player join')
# def handle_player_join(data):
#     name = data['playerName']
#     gameid = int(data['gameid'])
#     newPlayer = game_players(gameid=gameid, playername=name, questionsanswered=0)
#     db.session.add(newPlayer)
#     db.session.commit()
#     print("player name: " + name)
#     return redirect('/game/' + str(gameid) + '/waiting_room/' + str(newPlayer.playerid))

@socketio.on("connect waiting room")
def handle_connect_waiting_room(data):
    gameid = int(data["gameid"])
    waitingrooms[gameid] = request.sid

@main.route('/game/<gameid>/join', methods=['POST'])
def join_game_post(gameid):
    name = request.form.get('playername')
    newPlayer = game_players(gameid=gameid, playername=name, questionsanswered=0)
    db.session.add(newPlayer)
    db.session.commit()
    print("player name: " + name)


    # THE PROBLEM IS HERE
    # THE PLAYER JOINED SOCKET IS SENT TO ALL INSTANCES OF GAME.HTML
    # NEEDS TO BE ONLY SENT TO THE ONE WITH THAT SPECIFIC GAMEID

    socketio.emit("player joined", name, to=waitingrooms[int(gameid)])
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

@main.route('/game/<gameid>/competition/<playerid>', methods=['GET'])
def compeition_player(gameid, playerid):
    questions = Games.query.filter_by(gameid=gameid).all()
    data = []
    for question in questions:
        title = (Questions.query.filter_by(questionid=question.gamequestions).first().title)
        description = (Questions.query.filter_by(questionid=question.gamequestions).first().description)
        questionId = str(Questions.query.filter_by(questionid=question.gamequestions).first().questionid)
        data.append({"title": title, "description": description, "questionId": questionId})
    return render_template('competition.html', data=data, gameid=gameid, playerid=playerid)

@socketio.on("leaderboard connect")
def handle_leaderboard_connect(data):
    gameid = int(data["gameid"])
    leaderboardrooms[gameid] = request.sid

@main.route('/game/<gameid>/competition/<playerid>', methods=['POST'])
def compeition_player_post(gameid, playerid):
    data = request.get_json()
    questionName = data['question']
    questionAnswer = data['answer']
    questions = Questions.query.filter_by(title = questionName).first()
    if int(questions.answers) == int(questionAnswer):
        print("correct")
        db.session.query(game_players).filter(game_players.playerid == playerid).update({'questionsanswered': game_players.questionsanswered + 1})
        print(f"{questionName}+correct")
        playerName = game_players.query.filter_by(playerid=playerid).first().playername

        #NEED TO EMIT THIS TO THE CORRECT SOCKET ONLY

        socketio.emit('question answered', {'question': questionName, 'player': playerName}, to=leaderboardrooms[int(gameid)])
        
        
        db.session.commit()
        return f"{questionName}+correct"
    else:
        print("incorrect")
        return f"{questionName}+incorrect"

@main.route('/game/<gameid>/competition/leaderboard')
@login_required
def leaderboard(gameid):
    players = game_players.query.filter_by(gameid=gameid).all()
    numberOfQuestions = len(Games.query.filter_by(gameid=gameid).all())
    playerNames = []
    playerScores = []
    for player in players:
        playerNames.append(player.playername)
        playerScores.append(player.questionsanswered)
    return render_template('hostGamePage.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, numberOfQuestions=numberOfQuestions)

@main.route("/game/<gameid>/leaderboard/players")
def endGameLeaderboard(gameid):
    print(f"endgame leaderboard gameid arg: {gameid}")
    players = game_players.query.filter_by(gameid=gameid).all()
    playerNames = []
    playerScores = []
    for player in players:
        playerNames.append(player.playername)
        playerScores.append(player.questionsanswered)
    print(playerNames)
    print(playerScores)
    return render_template('playerLeaderboard.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores)



# @main.route('/game/<gameid>/competition/leaderboard', methods=['POST'])
# @login_required
# def leaderboard_post():
#     players = game_players.query.filter_by(gameid=gameid).all()
#     playerNames = []
#     playerScores = []
#     for player in players:
#         playerNames.append(player.playername)
#         playerScores.append(player.questionsanswered)
#     return render_template('hostGamePage.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores)



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
    