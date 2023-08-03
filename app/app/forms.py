from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(message="Email invalid."),
        ],
    )


class ProfileForm(FlaskForm):
    firstname = StringField(
        "Vorname",
        validators=[
            InputRequired(),
        ],
    )
    lastname = StringField(
        "Nachname",
        validators=[
            InputRequired(),
        ],
    )
    scoutname = StringField(
        "Pfadiname",
        validators=[
            InputRequired(),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(message="Not a valid email address."),
        ],
    )
    phone = StringField("Mobile", validators=[InputRequired()])
    recaptcha = RecaptchaField()
