from flask import Blueprint, render_template, request, redirect, jsonify, current_app
from flask_login import login_required, current_user
from .myapp import db
from .models import Questions, Games, game_players, Users
#from sqlalchemy import update, func
from random import randint
import requests
from flask_socketio import SocketIO, join_room
from .myapp import socketio
from .writeFiles import Q4, Q5, Q6, Q7, Q8, Q9, Q10


main = Blueprint('main', __name__)
rooms = {}
waitingrooms = {}
leaderboardrooms = {}
waitingRoomPlayers = {}
winners = {}
timeincrease = {}
questionOrder = {}


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    playtime = Users.query.filter_by(personid=current_user.personid).first().playtime
    wins = Users.query.filter_by(personid=current_user.personid).first().wins
    return render_template('profile.html', name=current_user.name, playtime=playtime, wins=wins)

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
    questionOrder[gameid] = {}
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
    seconds = request.form.get('timer_seconds')
    print(f"seconds: {seconds}")
    minutes = request.form.get('timer_minutes')
    print(f"minutes: {minutes}")
    totaltime = int(seconds) + (int(minutes) * 60)
    db.session.query(Games).filter(Games.gameid == gameid).update({'duration': totaltime})
    db.session.commit()
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

@socketio.on("connect waiting room players")
def handle_connect_waiting_room_players(data):
    gameid = int(data["gameid"])
    playerid = int(data["playerid"])
    waitingRoomPlayers[playerid] = request.sid
    print(f"waiting room players: {waitingRoomPlayers}")
    socketio.emit("player joined waiting room", to=request.sid)
# @main.route('/game/<gameid>/waiting_room/<playerid>', methods=['POST'])
# def waiting_room_post(gameid, playerid):
#     try:
#         if gameStarted == True:
#             return redirect('/game/' + str(gameid) + '/competition/' + str(playerid))
#         else:
#             return render_template('waiting_room.html', gameid=gameid, playerid=playerid, waitWarning="Please wait for the host to start the game")
#     except:
#         return render_template('waiting_room.html', gameid=gameid, playerid=playerid, waitWarning="Please wait for the host to start the game")

@main.route('/game/<gameid>/competition', methods=['POST'])
def competition(gameid):
    # global gameStarted
    # gameStarted = True
    print("testing game start post request")
    print(f"waiting room players: {waitingRoomPlayers}")
    for player in waitingRoomPlayers:
        print(f"player: {player}")
        print(f"sid: {waitingRoomPlayers[player]}")
        socketio.emit("game started", data={"gameid": gameid, "playerid":player}, to=waitingRoomPlayers[player])
    return redirect('/game/' + str(gameid) + '/competition/leaderboard')

@main.route('/game/<gameid>/competition/<playerid>', methods=['GET'])
def competition_player(gameid, playerid):
    questions = Games.query.filter_by(gameid=gameid).all()
    data = []
    gameduration = Games.query.filter_by(gameid=gameid).first().duration
    print(f"game duration: {gameduration}")
    for question in questions:
        title = (Questions.query.filter_by(questionid=question.gamequestions).first().title)
        description = (Questions.query.filter_by(questionid=question.gamequestions).first().description)
        questionId = str(Questions.query.filter_by(questionid=question.gamequestions).first().questionid)
        data.append({"title": title, "description": description, "questionId": questionId})
    return render_template('competition.html', data=data, gameid=gameid, playerid=playerid, duration=gameduration)

@socketio.on("finished questions")
def handle_finished_questions(data):
    gameid = int(data["gameid"])
    playerid = int(data["playerid"])
    if gameid not in winners:
        winners[gameid] = playerid
        handle_increase_wins(data)

@socketio.on("leaderboard connect")
def handle_leaderboard_connect(data):
    gameid = int(data["gameid"])
    leaderboardrooms[gameid] = request.sid

@main.route('/game/<gameid>/competition/<playerid>', methods=['POST'])
def competition_player_post(gameid, playerid):
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
    
@socketio.on("correct answer")
def handle_correct_answer(data):
    questionName = data['question']
    playerid = data['playerId']
    gameid = int(data['gameId'])
    questionid = data["questionid"]
    if questionid not in questionOrder[gameid]:
        questionOrder[gameid][questionid] = [playerid]
    else:
        questionOrder[gameid][questionid].append(playerid)
    questions = Questions.query.filter_by(title = questionName).first()
    db.session.query(game_players).filter(game_players.playerid == playerid).update({'questionsanswered': game_players.questionsanswered + 1})
    db.session.commit()
    print(f"player id index: {questionOrder[gameid][questionid].index(playerid)}")
    print(f"floor div using index + 1: {1000 // (questionOrder[gameid][questionid].index(playerid) + 1)}")
    questionScore = (1000 // (questionOrder[gameid][questionid].index(playerid) + 1))
    print(f"question score: {questionScore}")
    db.session.query(game_players).filter(game_players.playerid == playerid).update({'score': game_players.score + questionScore})
    db.session.commit()
    playerName = game_players.query.filter_by(playerid=playerid).first().playername
    socketio.emit('question answered', {'question': questionName, 'player': playerName, 'score': questionScore}, to=leaderboardrooms[int(gameid)])
    

@main.route('/game/<gameid>/competition/leaderboard')
@login_required
def leaderboard(gameid):
    players = game_players.query.filter_by(gameid=gameid).all()
    numberOfQuestions = len(Games.query.filter_by(gameid=gameid).all())
    playerNames = []
    playerScores = []
    for player in players:
        playerNames.append(player.playername)
        playerScores.append(player.score)
    return render_template('hostGamePage.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, numberOfQuestions=numberOfQuestions)

@main.route("/game/<gameid>/leaderboard/players")
def endGameLeaderboard(gameid):
    print(f"endgame leaderboard gameid arg: {gameid}")
    players = game_players.query.filter_by(gameid=gameid).all()
    playerNames = []
    playerScores = []
    results = {}
    for player in players:
        playerNames.append(player.playername)
        playerScores.append(player.questionsanswered)
        results[player.playername] = player.score
    sortedResults = sorted(results.items(), key=lambda x: x[1], reverse=True)
    print(playerNames)
    print(playerScores)
    print(sortedResults)
    return render_template('playerLeaderboard.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, results=sortedResults)

@main.route("/joingame")
def joinGame():
    return render_template('joinGame.html')

@main.route("/joingame", methods=['POST'])
def joinGamePost():
    gameid = request.form.get('gameid')
    print(gameid)
    return redirect('/game/' + str(gameid) + '/join')


@socketio.on("change input")
def handle_new_question(data):
    questionid = data["questionId"]
    playerid = data["playerId"]
    questionFileMatch = {"4": Q4(playerid), "5": Q5(playerid), "6": Q6(playerid), "7": Q7(playerid), "8": Q8(playerid), "9": Q9(playerid), "10": Q10(playerid)}
    answer = questionFileMatch[questionid]
    print("changed input")
    socketio.emit("question answer", {"questionId": questionid, "answer": answer}, to=request.sid)

#this may not need to be a socket - not being used as one currently
# @socketio.on("increase wins")
def handle_increase_wins(data):
    playerid = data["playerid"]
    email = current_user.email
    print(email)
    db.session.query(Users).filter(Users.email == email).update({'wins': Users.wins + 1})
    db.session.commit()
    print("increased wins")

@socketio.on("increase playtime")
def handle_increase_time(data):
    playerid = data["playerid"]
    gametime = data["gametime"]
    gameid = data["gameid"]
    email = current_user.email
    if gameid not in timeincrease:
        db.session.query(Users).filter(Users.email == email).update({'playtime': Users.playtime + gametime})
        db.session.commit()
        timeincrease[gameid] = {playerid: True}
        print("increased time")
    elif playerid not in timeincrease[gameid]:
        db.session.query(Users).filter(Users.email == email).update({'playtime': Users.playtime + gametime})
        db.session.commit()
        timeincrease[gameid][playerid] = True
        print("increased time")

@main.route('/scoring')
def scoring():
    return render_template('scoring.html')
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
    