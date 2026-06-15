from flask import Flask,render_template
from data import player_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/players")
def player():
    data = player_data
    return render_template('players.html',players = data)

@app.route("/player/<int:player_id>")
def show_player(player_id):
    req_player = None
    data = player_data
    for player in data:
        if player['id']==player_id:
            req_player = player
    if req_player is None:
        return 'Player Not Found',404

    return render_template('player_info.html',player=req_player)


if __name__ == '__main__':
    app.run(debug = True)