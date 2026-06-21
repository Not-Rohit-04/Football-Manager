from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    IntegerField,
    BooleanField,
    TextAreaField,
    PasswordField,
)
from wtforms.validators import DataRequired


class AddPlayer(FlaskForm):
    name = StringField("Player Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    nation = StringField("Nation", validators=[DataRequired()])
    club = StringField("Club", validators=[DataRequired()])
    position = SelectField(
        "Position",
        choices=[
            ("GK", "GK"),
            ("CB", "CB"),
            ("CM", "CM"),
            ("CAM", "CAM"),
            ("LW", "LW"),
            ("RW", "RW"),
            ("ST", "ST"),
        ],
    )
    image_url = StringField("Image URL")
    short_desc = StringField("Short Description")
    about = TextAreaField("About")
    legend = BooleanField("Legend")
    submit = SubmitField("Add Player")


class EditPlayer(FlaskForm):
    age = IntegerField("Age", validators=[DataRequired()])
    rating = IntegerField("Rating", validators=[DataRequired()])
    nation = StringField("Nation", validators=[DataRequired()])
    club = StringField("Club", validators=[DataRequired()])
    position = SelectField(
        "Position",
        choices=[
            ("GK", "GK"),
            ("CB", "CB"),
            ("CM", "CM"),
            ("CAM", "CAM"),
            ("LW", "LW"),
            ("RW", "RW"),
            ("ST", "ST"),
        ]
    )
    image_url = StringField("Image URL")
    short_desc = StringField("Short Description")
    about = TextAreaField("About")
    legend = BooleanField("Legend")
    submit = SubmitField("Update")


class LoginForm(FlaskForm):
    name = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")
