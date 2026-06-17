from flask import Flask,render_template
from data import player_data
from form import AddPlayer
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os

app = Flask(__name__)
bootstrap=Bootstrap5(app)
load_dotenv()

app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")

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

@app.route("/build-team")
def build_team():
    return render_template('build_team.html')

@app.route("/hof-team")
def hall_of_fame():
    return render_template('hof_team.html')

@app.route("/mix-team")
def mix_team():
    return render_template('mix_team.html')

@app.route("/add-player")
def add_player():
    form = AddPlayer()
    return render_template('add.html',form=form)

print(app.config['SECRET_KEY'])
if __name__ == '__main__':
    app.run(debug = True)