from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from data import seed_player
import random

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///players.db"
db.init_app(app)


class Player(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    nation: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[str] = mapped_column(String(10), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    club: Mapped[str] = mapped_column(String(100), nullable=False)


with app.app_context():
    db.create_all()

    if Player.query.count() == 0:
        seed_player(Player, db)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/players")
def player():
    result = db.session.execute(db.select(Player))
    all_players = result.scalars().all()
    return render_template("players.html", all_players=all_players)


@app.route("/build-team", methods=["GET", "POST"])
def build_team():

    goalkeepers = (
        db.session.execute(db.select(Player).where(Player.position == "GK"))
        .scalars()
        .all()
    )
    defenders = (
        db.session.execute(
            db.select(Player).where(Player.position.in_(["CB", "RB", "LB"]))
        )
        .scalars()
        .all()
    )
    midfielders = (
        db.session.execute(
            db.select(Player).where(Player.position.in_(["CM", "CAM", "CDM"]))
        )
        .scalars()
        .all()
    )
    attackers = (
        db.session.execute(
            db.select(Player).where(Player.position.in_(["ST", "LW", "RW"]))
        )
        .scalars()
        .all()
    )

    goalkeepers = random.sample(goalkeepers, 3)

    defenders = random.sample(defenders, 3)

    midfielder_1 = random.sample(midfielders, 3)

    midfielder_2 = random.sample(midfielders, 3)

    attackers = random.sample(attackers, 3)

    if request.method == "POST":

        gk_id = request.form.get("goalkeeper")
        def_id = request.form.get("defender")
        mid_id_1 = request.form.get("midfielder1")
        mid_id_2 = request.form.get("midfielder2")
        atk_id = request.form.get("attacker")

        sel_gk = db.get_or_404(Player, gk_id)
        sel_def = db.get_or_404(Player, def_id)
        sel_mid_1 = db.get_or_404(Player, mid_id_1)
        sel_mid_2 = db.get_or_404(Player, mid_id_2)
        sel_atk = db.get_or_404(Player, atk_id)

        session["gk_id"] = sel_gk.id
        session["def_id"] = sel_def.id
        session["mid_id_1"] = sel_mid_1.id
        session["mid_id_2"] = sel_mid_2.id
        session["atk_id"] = sel_atk.id

        team_rating = round(
            (
                sel_gk.rating
                + sel_def.rating
                + sel_mid_1.rating
                + sel_mid_2.rating
                + sel_atk.rating
            )
            / 4,
            2,
        )
        return render_template(
            "team_view.html",
            gk=sel_gk,
            defe=sel_def,
            mid1=sel_mid_1,
            mid2=sel_mid_2,
            atk=sel_atk,
            team_rating=team_rating,
        )

    return render_template(
        "build_team.html",
        goalkeepers=goalkeepers,
        defenders=defenders,
        midfielder1=midfielder_1,
        midfielder2=midfielder_2,
        attackers=attackers,
    )


@app.route("/play-match", methods=["GET", "POST"])
def play_match():
    sel_gk = db.get_or_404(Player, session["gk_id"])
    sel_def = db.get_or_404(Player, session["def_id"])
    sel_mid_1 = db.get_or_404(Player, session["mid_id_1"])
    sel_mid_2 = db.get_or_404(Player, session["mid_id_2"])
    sel_atk = db.get_or_404(Player, session["atk_id"])

    computer_gk = random.choice(
        db.session.execute(db.select(Player).where(Player.position == "GK"))
        .scalars()
        .all()
    )
    computer_defe = random.choice(
        db.session.execute(
            db.select(Player).where(Player.position.in_(["CB", "RB", "LB"]))
        )
        .scalars()
        .all()
    )
    computer_mid_1 = random.choice(
        db.session.execute(
            db.select(Player).where(Player.position.in_(["CM", "CAM", "CDM"]))
        )
        .scalars()
        .all()
    )
    computer_mid_2 = random.choice(
        db.session.execute(
            db.select(Player).where(Player.position.in_(["CM", "CAM", "CDM"]))
        )
        .scalars()
        .all()
    )
    computer_atk = random.choice(
        db.session.execute(
            db.select(Player).where(Player.position.in_(["ST", "LW", "RW"]))
        )
        .scalars()
        .all()
    )
    computer_rating = round(
    (
        computer_gk.rating +
        computer_defe.rating +
        computer_mid_1.rating +
        computer_mid_2.rating +
        computer_atk.rating
    ) / 4,2)
    
    team_rating = round(
            (
                sel_gk.rating
                + sel_def.rating
                + sel_mid_1.rating
                + sel_mid_2.rating
                + sel_atk.rating
            )
            / 4,2,)
    
    your_score = random.randint(0,10)
    computer_score = random.randint(0, 10)
    
    if your_score > computer_score:
        result = "You Win!"
    elif computer_score > your_score:
        result = "Computer Wins!"
    else:
        result = "Draw!"
    
    return render_template("match.html",your_score=your_score,computer_score=computer_score,comp_rating=computer_rating,team_rating=team_rating,result=result,c_gk=computer_gk,c_def=computer_defe,cm_1=computer_mid_1,cm_2=computer_mid_2,c_atk=computer_atk,gk=sel_gk,defe=sel_def,mid_1=sel_mid_1,mid_2=sel_mid_2,atk=sel_atk)


@app.route("/hof-team", methods=["GET", "POST"])
def hall_of_fame():
    legend_players = (
        db.session.execute(db.select(Player).where(Player.legend == True))
        .scalars()
        .all()
    )
    return render_template("hof_team.html", legends=legend_players)


@app.route("/mix-team")
def mix_team():
    return render_template("mix_team.html")


if __name__ == "__main__":
    app.run(debug=True)
