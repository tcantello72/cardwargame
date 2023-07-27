"""
created by: Toby Cantello
Date created: 7/26/23
Last updated: 7/27/23
""" 

# Import required modules
from flask import Flask, render_template, session
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

    # Gets the Deck Id that was created when "/" route was accessed
    deckId = session.get('deckId', None)

    # Player 1 draws a card
    p1_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
    p1_card_select = requests.get(p1_card_req)
    p1_card = json.loads(p1_card_select.content)

    # Player 2 draws a card
    p2_card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
    p2_card_select = requests.get(p2_card_req)
    p2_card = json.loads(p2_card_select.content)
    return render_template("play.html", p1_card=p1_card, p1_cards=p1_card['cards'], p2_card=p2_card, p2_cards=p2_card['cards'])

# Starts the server
if __name__ == "__main__":
    app.run(debug=True)