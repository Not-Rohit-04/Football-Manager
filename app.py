from flask import Flask,render_template,redirect,url_for,session
from data import player_data
from form import AddPlayer,EditPlayer,LoginForm
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean,Text

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
    rating: Mapped[int] = mapped_column(Integer,nullable=False)
    position: Mapped[str] = mapped_column(String(10),nullable=False)
    nation: Mapped[str] = mapped_column(String(50),nullable=False)
    img: Mapped[str] = mapped_column(String(500),nullable=False)
    about: Mapped[str] = mapped_column(Text,nullable=False)
    age: Mapped[int] = mapped_column(Integer,nullable=False)
    club: Mapped[str] = mapped_column(String(100),nullable=False)
    description: Mapped[str] = mapped_column(String(500),nullable=False)
    
    legend: Mapped[bool] = mapped_column(Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/players")
def player():
    result = db.session.execute(db.select(Player))
    all_players=result.scalars().all()
    return render_template('players.html',all_players = all_players)

@app.route("/player/<int:player_id>")
def show_player(player_id):
    req_player = db.get_or_404(Player,player_id)
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

@app.route("/add-player",methods=['GET','Post'])
def add_player():
    if not session.get('admin'):
        return redirect(url_for('login'))
    form = AddPlayer()
    if form.validate_on_submit():
        new_player=Player(
            name = form.name.data,
            rating = form.rating.data,
            age = form.age.data,
            nation = form.nation.data,
            position = form.position.data,
            club=form.club.data,
            img=form.image_url.data,
            description=form.short_desc.data,
            about = form.about.data,
            legend = form.legend.data
        )
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('add_player'))

    return render_template('add.html',form=form)


@app.route("/edit-player/<int:player_id>",methods=['GET','POST'])
def edit_player(player_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    req_player = db.get_or_404(Player,player_id)
    edit_form = EditPlayer(
        age = req_player.age,
        rating = req_player.rating,
        nation = req_player.nation,
        club = req_player.club,
        position = req_player.position,
        image_url = req_player.img,
        short_desc = req_player.description,
        about = req_player.about,
        legend = req_player.legend
    )
    if edit_form.validate_on_submit():
        req_player.age = edit_form.age.data
        req_player.rating = edit_form.rating.data
        req_player.nation = edit_form.nation.data
        req_player.club = edit_form.club.data
        req_player.position = edit_form.position.data
        req_player.img = edit_form.image_url.data
        req_player.description = edit_form.short_desc.data
        req_player.about = edit_form.about.data
        req_player.legend = edit_form.legend.data
        db.session.commit()
        return redirect(url_for("show_player",player_id=req_player.id))
    return render_template('edit.html',form=edit_form,player=req_player)

@app.route("/delete-player/<int:player_id>")
def delete_player(player_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    req_player = db.get_or_404(Player,player_id)
    db.session.delete(req_player)
    db.session.commit()
    return redirect(url_for('player'))


@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    ad_name = os.getenv('ADMIN_USERNAME')
    ad_pass = os.getenv('ADMIN_PASSWORD')
    if form.validate_on_submit():
        if form.name.data == ad_name and form.password.data == ad_pass:
            session['admin'] = True
            return redirect(url_for('home'))
        
    return render_template('login.html',form = form)


@app.route("/logout")
def logout():
    session.pop("admin",None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)