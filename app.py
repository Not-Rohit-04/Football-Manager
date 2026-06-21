from flask import Flask,render_template
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from data import seed_player


load_dotenv()

app = Flask(__name__)
bootstrap=Bootstrap5(app)
app.config["SECRET_KEY"]=os.getenv("SECRET_KEY")

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///players.db"
db.init_app(app)


class Player(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100),nullable=False)
    age: Mapped[int] = mapped_column(Integer,nullable=False)
    nation: Mapped[str] = mapped_column(String(50),nullable=False)
    position: Mapped[str] = mapped_column(String(10),nullable=False)
    rating: Mapped[int] = mapped_column(Integer,nullable=False)
    club: Mapped[str] = mapped_column(String(100),nullable=False)

with app.app_context():
    db.create_all()
    
    if Player.query.count() == 0:
        seed_player(Player,db)



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/players")
def player():
    result = db.session.execute(db.select(Player))
    all_players=result.scalars().all()
    return render_template('players.html',all_players = all_players)

@app.route("/build-team",methods=["GET","POST"])
def build_team():
    pass

@app.route("/hof-team",methods=['GET','POST'])
def hall_of_fame():
    legend_players = db.session.execute(db.select(Player).where(Player.legend==True)).scalars().all()
    return render_template('hof_team.html',legends=legend_players)

@app.route("/mix-team")
def mix_team():
    return render_template('mix_team.html')


if __name__ == '__main__':
    app.run(debug = True)