"""
created by: Toby Cantello
Date created: 7/26/23
Last updated: 8/17/23
""" 

# Import required modules
from flask import Flask, render_template, request, redirect, session
import requests
import json
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Create a flask application, connect to database, enter secert key, Intitial flask-sqlalchemy extension
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cardgame.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'YumRocks2023!'
db = SQLAlchemy()

# Global score variables
globalPlayer1Wins = 0
globalPlayer1Losses = 0
globalPlayer1Ties = 0
globalPlayer2Wins = 0
globalPlayer2Losses = 0
globalPlayer2Ties = 0

# Initialize app with extension   
db.init_app(app)

class PlayerWins(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    player = db.Column("player", db.String(10))
    wins = db.Column("wins", db.Integer)
    losses = db.Column("losses", db.Integer)
    ties = db.Column("ties", db.Integer)

class Comments(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(50))
    email = db.Column("email", db.String(50))
    userComment = db.Column("userComment", db.String(300))

# Create database within app context 
with app.app_context():
    db.create_all()

# Routes
@app.route("/", methods=["POST", "GET"])
def index():
    global globalPlayer1Wins
    global globalPlayer1Losses
    global globalPlayer1Ties
    global globalPlayer2Wins
    global globalPlayer2Losses
    global globalPlayer2Ties

    # Request is made to the API for a new deck of cards
    deck_req = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle')
    deck = json.loads(deck_req.content)
    deckId = deck['deck_id']
    session['deckId'] = deckId

    globalPlayer1Wins = 0
    globalPlayer1Losses = 0
    globalPlayer1Ties = 0
    globalPlayer2Wins = 0
    globalPlayer2Losses = 0
    globalPlayer2Ties = 0

    return render_template("index.html")

@app.route("/play", methods=["POST", "GET"])
def play():
 
    hand = {"ACE": 14, "KING": 13, "QUEEN": 12, "JACK": 11, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3":3, "2": 2, "": 0}
    global globalPlayer1Wins
    global globalPlayer1Losses
    global globalPlayer1Ties
    global globalPlayer2Wins
    global globalPlayer2Losses
    global globalPlayer2Ties

    if request.method == "POST":
        # Gets the Deck Id that was created when "/" route was accessed
        deckId = session.get('deckId', None)
    
        # Getting Player Names
        p1Name = request.form.get("p1name")
        p2Name = request.form.get("p2name")
        session['p1Name'] = p1Name
        session['p2Name'] = p2Name

        # Player 1 draws a card
        p1_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p1_card_select = requests.get(p1_card_req)
        p1_card = json.loads(p1_card_select.content)
        p1value = p1_card['cards'][0]['value']
        p1valuescore = hand[p1value]
    
        # Player 2 draws a card
        p2_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p2_card_select = requests.get(p2_card_req)
        p2_card = json.loads(p2_card_select.content)
        p2value = p2_card['cards'][0]['value']
        p2valuescore = hand[p2value]

        if p1valuescore > p2valuescore:
            globalPlayer1Wins += 1
            globalPlayer2Losses += 1
        elif p1valuescore < p2valuescore:
            globalPlayer1Losses += 1
            globalPlayer2Wins += 1
        elif p1valuescore == p2valuescore:
            globalPlayer1Ties += 1
            globalPlayer2Ties += 1

        return render_template("play.html", p1_card=p1_card, p1_cards=p1_card['cards'], p2_card=p2_card, p2_cards=p2_card['cards'], p1Name=p1Name, p2Name=p2Name, p1value=p1value, p2value=p2value, p1valuescore=p1valuescore, p2valuescore=p2valuescore, 
            player1wins=globalPlayer1Wins, player1losses=globalPlayer1Losses, player1ties=globalPlayer1Ties, player2wins=globalPlayer2Wins, player2losses=globalPlayer2Losses, player2ties=globalPlayer2Ties)
    
    else:
        # Gets the Deck Id that was created when "/" route was accessed
        deckId = session.get('deckId', None)

        # Getting Player Names
        p1Name = session.get('p1Name', None)
        p2Name = session.get('p2Name', None)       
    
        # Player 1 draws a card
        p1_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p1_card_select = requests.get(p1_card_req)
        p1_card = json.loads(p1_card_select.content)
        p1value = p1_card['cards'][0]['value']
        p1valuescore = hand[p1value]
    

        # Player 2 draws a card
        p2_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p2_card_select = requests.get(p2_card_req)
        p2_card = json.loads(p2_card_select.content)
        p2value = p2_card['cards'][0]['value']
        p2valuescore = hand[p2value]

        if p1valuescore > p2valuescore:
            globalPlayer1Wins += 1
            globalPlayer2Losses += 1
        elif p1valuescore < p2valuescore:
            globalPlayer1Losses += 1
            globalPlayer2Wins += 1
        elif p1valuescore == p2valuescore:
            globalPlayer1Ties += 1
            globalPlayer2Ties += 1

        return render_template("play.html", p1_card=p1_card, p1_cards=p1_card['cards'], p2_card=p2_card, p2_cards=p2_card['cards'], p1Name=p1Name, p2Name=p2Name, p1value=p1value, p2value=p2value, p1valuescore=p1valuescore, p2valuescore=p2valuescore,
            player1wins=globalPlayer1Wins, player1losses=globalPlayer1Losses, player1ties=globalPlayer1Ties, player2wins=globalPlayer2Wins, player2losses=globalPlayer2Losses, player2ties=globalPlayer2Ties)

@app.route("/howto", methods=["POST", "GET"])
def howto():
    return render_template("howto.html")

@app.route("/creator", methods=["POST", "GET"])
def creator():
    return render_template("creator.html")

@app.route("/comments", methods=["POST", "GET"])
def comments():
    if request.method =='POST':
        comment = Comments(
            name = request.form['name'],
            email = request.form['email'],
            userComment = request.form['userComment'],
            )
        
        try:
            db.session.add(comment)
            db.session.commit()
            return redirect('/comments')
        except:
            return 'There was an issue adding your comment'    
    else:
        comments = Comments.query.order_by(Comments.id).all()
        return render_template('comments.html', comments=comments)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#  Starts the server
if __name__ == "__main__":
    app.run(debug=True)