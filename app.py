"""
created by: Toby Cantello
Date created: 7/26/23
Last updated: 7/26/23
""" 

# Import required modules
from flask import Flask, render_template
import requests
import json

# Flask Object creation
app = Flask(__name__)

# Routes
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST", "GET"])
def play():
    deck_req = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle')
    deck = json.loads(deck_req.content)
    deckId = deck['deck_id']
    card_req = f'https://deckofcardsapi.com/api/deck/{deckId}/draw/?count=1'
    card_select = requests.get(card_req)
    card = json.loads(card_select.content)
    print(card)
   
    return render_template("play.html", deck=deck, card=card, cards=card['cards'])

# Starts the server
if __name__ == "__main__":
    app.run(debug=True)