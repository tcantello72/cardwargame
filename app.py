"""
created by: Toby Cantello
Date created: 7/26/23
Last updated: 8/2/23
""" 

# Import required modules
from flask import Flask, render_template, redirect, url_for, request, session
import requests
import json

# Flask Object creation
app = Flask(__name__)

# Setting Secert Key 
app.secret_key = 'YumRocks2023!'

# Routes
@app.route("/", methods=["POST", "GET"])
def index():

    # Request is made to the API for a new deck of cards
    deck_req = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle')
    deck = json.loads(deck_req.content)
    deckId = deck['deck_id']
    session['deckId'] = deckId
    return render_template("index.html")

@app.route("/play", methods=["POST", "GET"])
def play():

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

        # Player 2 draws a card
        p2_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p2_card_select = requests.get(p2_card_req)
        p2_card = json.loads(p2_card_select.content)
        return render_template("play.html", p1_card=p1_card, p1_cards=p1_card['cards'], p2_card=p2_card, p2_cards=p2_card['cards'], p1Name=p1Name, p2Name=p2Name)
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

        # Player 2 draws a card
        p2_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
        p2_card_select = requests.get(p2_card_req)
        p2_card = json.loads(p2_card_select.content)
        return render_template("play.html", p1_card=p1_card, p1_cards=p1_card['cards'], p2_card=p2_card, p2_cards=p2_card['cards'], p1Name=p1Name, p2Name=p2Name)

@app.route("/creator", methods=["POST", "GET"])
def creator():
    return render_template("creator.html")

@app.route("/howto", methods=["POST", "GET"])
def howto():
    return render_template("howto.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

#  Starts the server
if __name__ == "__main__":
    app.run(debug=True)