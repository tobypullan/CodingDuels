from flask import Blueprint, render_template, request, redirect, jsonify, current_app, flash, url_for
from flask_login import login_required, current_user
from .myapp import db
from .models import Questions, Games, game_players, Users
#from sqlalchemy import update, func
from random import randint
import requests
from flask_socketio import SocketIO, join_room
from .myapp import socketio
from .writeFiles import Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15
import os


main = Blueprint('main', __name__)
rooms = {} # gameid: sid contains the different games with their respective game creator's sids
waitingrooms = {} # contains the different gameids and their respective waiting room sids
leaderboardrooms = {} # contains the different gameids and their respective leaderboard sids
waitingRoomPlayers = {} # contains the different playerids and their respective waiting room sids
winners = {} # contains the different gameids and their respective winners
timeincrease = {} # contains the different gameids and their respective playerids
questionOrder = {} # contains the different gameids which contain the different questionids and their respective playerids
competitionPlayers = {} # contains the differnet gameids and an array of their respective player sids

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    playtime = Users.query.filter_by(personid=current_user.personid).first().playtime
    wins = Users.query.filter_by(personid=current_user.personid).first().wins
    return render_template('profile.html', name=current_user.name, playtime=playtime, wins=wins)


# CREATING A GAME

@main.route('/create')
@login_required
def create():
    questionData = Questions.query.all()
    return render_template('create.html', questionData=questionData)

@socketio.on("create game")
def handle_create_game():
    gameid = randint(0, 1000000000)
    questionOrder[gameid] = {} # storing gameid and creating the next layer of dictionary that contains the questionids and their respective playerids
    join_room(gameid)
    rooms[gameid] = request.sid # adding the gameid and the sid of the game creator to the rooms dictionary
    print(rooms)
    socketio.emit("game created", {"gameid": gameid}, to=request.sid) # sending the gameid back to the game creator

@socketio.on("select question")
def handle_select_question(data):
    print(rooms)
    questionid = Questions.query.filter_by(title=data["title"]).first()
    newGameQuestion = Games(gameid=data["gameid"], gamequestions=questionid.questionid, personid=current_user.personid) # adding the gameid, questionid and personid to the Games table by creating new object
    db.session.add(newGameQuestion)
    db.session.commit() # committing the object to the database
    socketio.emit("question selected", {"title": questionid.title, "description": questionid.description, "difficulty": questionid.difficulty}, to=request.sid)

@socketio.on("remove question")
def handle_remove_question(questionTitle):
    questionid = Questions.query.filter_by(title=questionTitle["title"]).first()
    difficulty = questionid.difficulty
    description = questionid.description
    db.session.query(Games).filter(Games.gamequestions == questionid.questionid).delete()
    db.session.commit()
    socketio.emit("question removed", {"title": questionid.title, "description": description, "difficulty": difficulty}, to=request.sid)

@main.route('/start_game', methods=['POST'])
@login_required
def start_game():
    gameid = request.form.get('gameid')
    seconds = request.form.get('timer_seconds')
    print(f"seconds: {seconds}")
    minutes = request.form.get('timer_minutes')
    print(f"minutes: {minutes}")
    broadcast = request.form.get('broadcast')
    if broadcast == "on": # checking if the broadcast checkbox is checked
        broadcast = True
    else:
        broadcast = False
    
    fullResults = request.form.get('fullResults') # checking if the full results checkbox is checked
    if fullResults == "on":
        fullResults = True
    else:
        fullResults = False
    
    print(f"broadcast: {broadcast}")
    print(f"fullResults: {fullResults}")
    totaltime = int(seconds) + (int(minutes) * 60)
    db.session.query(Games).filter(Games.gameid == gameid).update({'duration': totaltime, 'broadcast': broadcast, 'fullresults': fullResults}) # updating the duration, broadcast and fullresults columns in the Games table
    db.session.commit()
    print(f"start game gameid: {gameid}")
    redirect_url = '/game/' + str(gameid)
    return redirect(redirect_url)


@socketio.on("connect waiting room")
def handle_connect_waiting_room(data):
    gameid = int(data["gameid"])
    waitingrooms[gameid] = request.sid # adding the gameid and the sid of the waiting room to the waitingrooms dictionary

@main.route('/game/<gameid>') # page where gameid, questions, players in game are displayed and waiting for game to begin
@login_required
def game(gameid):
    questions = Games.query.filter_by(gameid=gameid).all()
    questionTitles = [] # storing the titles of the questions that are in the game
    for question in questions:
        questionTitles.append(Questions.query.filter_by(questionid=question.gamequestions).first().title)
    return render_template('game.html', questions=questionTitles, gameid=gameid)

# JOINING A GAME

@main.route("/joingame") # the join page where the player enters the gameid
def joinGame():
    return render_template('joinGame.html')

@main.route("/joingame", methods=['POST'])
def joinGamePost():
    gameid = request.form.get('gameid')
    if gameid.isdigit() == False: # checking if the gameid entered contains any letters
        print("game id must be a number")
        flash("Game ID must be a number")
        return redirect(url_for('main.joinGame'))   
    game = Games.query.filter_by(gameid=gameid).first() # checking if the gameid entered exists
    if game is None: 
        print("game does not exist")
        flash("Game does not exist")
        return redirect(url_for('main.joinGame'))
    else:
        print(gameid)
        return redirect('/game/' + str(gameid) + '/join')

@main.route('/game/<gameid>/join') # the join page where the player enters their name
def join_game(gameid):
    return render_template('join.html', gameid=gameid)

@main.route('/game/<gameid>/join', methods=['POST']) # handles the player name and adds the player to the game
def join_game_post(gameid):
    name = request.form.get('playername')
    newPlayer = game_players(gameid=gameid, playername=name, score=0) # add the player that has just joined to the game players table
    db.session.add(newPlayer)
    db.session.commit()
    print("player name: " + name)
    socketio.emit("player joined", name, to=waitingrooms[int(gameid)]) # using waitingrooms dictionary to send the player name to only the correct game creator
    return redirect('/game/' + str(gameid) + '/waiting_room/' + str(newPlayer.playerid))

@socketio.on("join game")
def handle_join_game(data):
    gameid = data["gameid"]
    join_room(gameid)
    socketio.emit("game joined", {"success": True}, to=request.sid)
    print("player joined room")

# THE WAITING ROOM

@main.route('/game/<gameid>/waiting_room/<playerid>') # the waiting room where the player waits for the game to start
def waiting_room(gameid, playerid):
    return render_template('waiting_room.html', gameid=gameid, playerid=playerid)

@socketio.on("connect waiting room players")
def handle_connect_waiting_room_players(data):
    gameid = int(data["gameid"])
    playerid = int(data["playerid"])
    waitingRoomPlayers[playerid] = request.sid # players in the waiting room are added to the waitingRoomPlayers dictionary
    print(f"waiting room players: {waitingRoomPlayers}")
    socketio.emit("player joined waiting room", to=request.sid)

# PLAYING A GAME (PLAYER)

@socketio.on("connect competition")
def handle_connect_competition(data):
    gameid = int(data["gameid"])
    if gameid not in competitionPlayers:
        competitionPlayers[gameid] = [request.sid]
    else:
        competitionPlayers[gameid].append(request.sid) # adds the player to the competitionPlayers dictionary array combination
    print(f"competition players: {competitionPlayers}")

@main.route('/game/<gameid>/competition/<playerid>', methods=['GET'])
def competition_player(gameid, playerid):
    questions = Games.query.filter_by(gameid=gameid).all()
    data = [] # contains title, description and questionid of the questions in the game
    gameduration = Games.query.filter_by(gameid=gameid).first().duration
    print(f"game duration: {gameduration}")
    for question in questions:
        title = (Questions.query.filter_by(questionid=question.gamequestions).first().title)
        description = (Questions.query.filter_by(questionid=question.gamequestions).first().description)
        questionId = str(Questions.query.filter_by(questionid=question.gamequestions).first().questionid)
        data.append({"title": title, "description": description, "questionId": questionId}) # bundles all question data so that it can be easily passed to the competition.html page
    return render_template('competition.html', data=data, gameid=gameid, playerid=playerid, duration=gameduration)

@socketio.on("correct answer")
def handle_correct_answer(data):
    questionName = data['question']
    playerid = data['playerId']
    gameid = int(data['gameId'])
    questionid = data["questionid"]
    if questionid not in questionOrder[gameid]:
        questionOrder[gameid][questionid] = [playerid]
    else:
        questionOrder[gameid][questionid].append(playerid) # adds the player to the questionOrder so that the player's score can be calculated - players are added in order of answering the question
    questions = Questions.query.filter_by(title = questionName).first()
    # db.session.query(game_players).filter(game_players.playerid == playerid).update({'questionsanswered': game_players.questionsanswered + 1})
    # db.session.commit()
    print(f"player id index: {questionOrder[gameid][questionid].index(playerid)}")
    print(f"floor div using index + 1: {1000 // (questionOrder[gameid][questionid].index(playerid) + 1)}")
    questionScore = (1000 // (questionOrder[gameid][questionid].index(playerid) + 1)) # calculating the player's score based on the position they answered the question
    print(f"question score: {questionScore}")
    db.session.query(game_players).filter(game_players.playerid == playerid).update({'score': game_players.score + questionScore}) # adds the player's score to the game_players table
    db.session.commit()
    playerName = game_players.query.filter_by(playerid=playerid).first().playername
    socketio.emit('question answered', {'question': questionName, 'player': playerName, 'score': questionScore}, to=leaderboardrooms[int(gameid)])
    checkbroadcast = Games.query.filter_by(gameid=gameid).first().broadcast
    if checkbroadcast == True:
        for player in competitionPlayers[gameid]:
            if player != request.sid: # doesn't tell the player that answered the question correctly that they answered the question correctly
                socketio.emit('player correct answer', {'question': questionName, 'player': playerName, 'score': questionScore}, to=player) # sends the player's name and score to the other players in the game so that they can see the player has answered a question

@socketio.on("incorrect answer")
def handle_incorrect_answer(data):
    gameid = int(data["gameId"])
    questionName = data['question']
    playerid = data['playerId']
    playerName = game_players.query.filter_by(playerid=playerid).first().playername
    checkbroadcast = Games.query.filter_by(gameid=gameid).first().broadcast
    if checkbroadcast == True:
        for player in competitionPlayers[gameid]:
            if player != request.sid: # doesn't tell the player that answered the question incorrectly that they answered the question incorrectly
                socketio.emit('player incorrect answer', {'question': questionName, 'player': playerName}, to=player) # sends the player's name to the other players in the game so that they can see the player has answered a question incorrectly

@socketio.on("finished questions")
def handle_finished_questions(data):
    gameid = int(data["gameid"])
    playerid = int(data["playerid"])
    if gameid not in winners: # check if there is already a winner for that game
        winners[gameid] = playerid # updates dictionary so that if checked for another player, they don't get credited with winning
        handle_increase_wins(data) # function to increase the player's wins


def handle_increase_wins(data):
    playerid = data["playerid"]
    email = current_user.email
    print(email)
    db.session.query(Users).filter(Users.email == email).update({'wins': Users.wins + 1}) # increments the player's wins by 1
    db.session.commit()
    print("increased wins")

# PLAYING A GAME (HOST)

@main.route('/game/<gameid>/competition', methods=['POST'])
def competition(gameid):
    print("testing game start post request")
    print(f"waiting room players: {waitingRoomPlayers}")
    for player in waitingRoomPlayers:
        print(f"player: {player}")
        print(f"sid: {waitingRoomPlayers[player]}")
        socketio.emit("game started", data={"gameid": gameid, "playerid":player}, to=waitingRoomPlayers[player]) # sends game started message to all players in the waiting room for that game to trigger them to recirect to the game
    return redirect('/game/' + str(gameid) + '/competition/leaderboard')

@socketio.on("leaderboard connect")
def handle_leaderboard_connect(data):
    gameid = int(data["gameid"])
    leaderboardrooms[gameid] = request.sid # adds the gameid and the sid of the leaderboard to the leaderboardrooms dictionary so that the server can send socket messages to leaderboard

@main.route('/game/<gameid>/competition/leaderboard')
@login_required
def leaderboard(gameid):
    players = game_players.query.filter_by(gameid=gameid).all() # gets all the players in the game
    numberOfQuestions = len(Games.query.filter_by(gameid=gameid).all()) # gets the number of questions in the game as each question is stored as a separate row in the database
    playerNames = []
    playerScores = []
    for player in players: # loops through the players and adds their names and scores to the playerNames and playerScores arrays
        playerNames.append(player.playername)
        playerScores.append(player.score)
    return render_template('hostGamePage.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, numberOfQuestions=numberOfQuestions)

@socketio.on("change input")
def handle_new_question(data):
    questionid = data["questionId"]
    playerid = data["playerId"]
    # dictionary maps each questionID to its respective function
    questionFileMatch = {"4": Q4(playerid), "5": Q5(playerid), "6": Q6(playerid), "7": Q7(playerid), "8": Q8(playerid), "9": Q9(playerid), "10": Q10(playerid), "11": Q11(playerid), "12": Q12(playerid), "13": Q13(playerid), "14": Q14(playerid), "15": Q15(playerid)}
    answer = questionFileMatch[questionid]
    print("changed input")
    socketio.emit("question answer", {"questionId": questionid, "answer": answer}, to=request.sid) # sends only to the player that requested the questions

# ENDING A GAME

@socketio.on("increase playtime")
def handle_increase_time(data):
    playerid = data["playerid"]
    gametime = data["gametime"]
    gameid = data["gameid"]
    email = current_user.email
    print(f"gametime: {gametime} for playerid: {playerid} in gameid: {gameid}")
    if gameid not in timeincrease: # checks if the gameid is already in the timeincrease dictionary
        db.session.query(Users).filter(Users.email == email).update({'playtime': Users.playtime + gametime}) # increments the player's playtime by the gametime
        db.session.commit()
        timeincrease[gameid] = {playerid: True} # adds the gameid and the playerid to the timeincrease dictionary and creates dictionary for playerids to be added to
        # so that the player's time is only increased once
        print("increased time")
    elif playerid not in timeincrease[gameid]:
        db.session.query(Users).filter(Users.email == email).update({'playtime': Users.playtime + gametime})
        db.session.commit()
        timeincrease[gameid][playerid] = True # adds the playerid to the gameid in the timeincrease dictionary so that the player's time is only increased once
        print("increased time")

@socketio.on("remove files")
def handle_remove_files(data):
    playerid = data["playerid"]
    for i in range(4,14):
        print(f"removing project/static/{playerid}{i}.txt")
        os.remove(f"project/static/{playerid}{i}.txt") # removes the files that were created for the player's questions
    socketio.emit("removed files", to=request.sid) # once files have been removed, tell client so that can redirect to the leaderboard page

# THE PLAYER LEADERBOARD

@main.route("/game/<gameid>/leaderboard/players")
def endGameLeaderboard(gameid):
    fullresults = Games.query.filter_by(gameid=gameid).first().fullresults
    if fullresults == True: # check whether game creator wants full results to be displayed
        print(f"endgame leaderboard gameid arg: {gameid}")
        players = game_players.query.filter_by(gameid=gameid).order_by(game_players.score.desc()).all() # gets all the players in the game and orders them by score
        playerNames = []
        playerScores = []
        results = []
        for player in players:
            playerNames.append(player.playername)
            playerScores.append(player.score)
            results.append([player.playername, player.score]) # stores results in a way that can be handled by the table on leaderboard page easily
        playerNames = playerNames[:3] # takes only the top three players to be displayed on the bar chart
        playerScores = playerScores[:3]
        return render_template('playerLeaderboard.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, results=results)
    else:
        players = game_players.query.filter_by(gameid=gameid).order_by(game_players.score.desc()).limit(3)
        playerNames = []
        playerScores = []
        results = []
        for player in players:
            playerNames.append(player.playername)
            playerScores.append(player.score)
            results.append([player.playername, player.score])
        return render_template('playerLeaderboard.html', gameid=gameid, playerNames=playerNames, playerScores=playerScores, results=results)

# SCORING INSTRUCTIONS

@main.route('/scoring') # scoring instructions page
def scoring():
    return render_template('scoring.html')

