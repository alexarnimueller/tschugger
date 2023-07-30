from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError


class PDFonly(object):
    def __init__(self, message: str = None):
        if not message:
            message = "Only PDF files are allowed"
        self.message = message

    def __call__(self, form, field):
        if field.data is not None and field.data.filename.rsplit(".", 1)[1].lower() != "pdf":
            raise ValidationError(self.message)


class ApplicationForm(FlaskForm):
    token = HiddenField("Application Token")
    status = SelectField("Application Status", choices=["step1", "step2", "step3", "step4"])
    firstname = StringField(
        "First Name(s)",
        validators=[
            InputRequired(),
        ],
    )
    lastname = StringField(
        "Last Name(s)",
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
    phone = StringField("Phone")
    affiliation = StringField("Affiliation")
    street = StringField(
        "Street",
        validators=[
            InputRequired(),
        ],
    )
    appartment = StringField("Apartment / Suite etc.")
    zipcode = StringField(
        "Zip Code",
        validators=[
            InputRequired(),
        ],
    )
    city = StringField(
        "City",
        validators=[
            InputRequired(),
        ],
    )
    state = StringField("State / Province")
    cv = FileField("CV", validators=[FileRequired(), PDFonly()])
    message = TextAreaField("Message")
    membership = SelectField(
        "Membership Type",
        choices=[
            "Full membership including online journal: 50£",
            "Full membership including online and paper copy journal: 70£",
            "Student membership excluding journal: 15£",
            "Student membership including online journal: 30£",
            "Student membership including online and paper copy journal: 45£",
        ],
    )
    payment = SelectField("Payment Option", choices=["PayPal (preferred)", "Invoice"])
    referee1 = StringField(
        "Referee 1",
        validators=[
            InputRequired(),
        ],
    )
    referee2 = StringField(
        'Referee 2 (not required for Student Applications, enter "None")',
        validators=[
            InputRequired(),
        ],
    )
    recaptcha = RecaptchaField()


class StatusForm(FlaskForm):
    token = StringField("Application Token")
    recaptcha = RecaptchaField()


class ApplicationUpdateForm(FlaskForm):
    token = HiddenField("Application Token")
    status = SelectField("Application Status", choices=["step1", "step2", "step3", "step4"])
    firstname = StringField(
        "First Name(s)",
        validators=[
            InputRequired(),
        ],
    )
    lastname = StringField(
        "Last Name(s)",
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
    phone = StringField("Phone")
    affiliation = StringField("Affiliation")
    street = StringField(
        "Street",
        validators=[
            InputRequired(),
        ],
    )
    appartment = StringField("Apartment / Suite etc.")
    zipcode = StringField(
        "Zip Code",
        validators=[
            InputRequired(),
        ],
    )
    city = StringField(
        "City",
        validators=[
            InputRequired(),
        ],
    )
    state = StringField("State / Province")
    country = SelectField("Country", choices=list(sorted(set([c["name"] for c in countries]))))
    cv = StringField("CV")
    letter1 = StringField("Reference Letter 1")
    letter2 = StringField("Reference Letter 2")
    file = FileField("Upload New Document", validators=[PDFonly()])
    filetype = SelectField("Document Type", choices=["Letter1", "Letter2"])
    message = TextAreaField("Message")
    membership = SelectField(
        "Membership Type",
        choices=[
            "Full membership including online journal: 50£",
            "Full membership including online and paper copy journal: 70£",
            "Student membership excluding journal: 15£",
            "Student membership including online journal: 30£",
            "Student membership including online and paper copy journal: 45£",
        ],
    )
    payment = SelectField("Payment Option", choices=["PayPal (preferred)", "Invoice"])
    referee1 = StringField(
        "Referee 1",
        validators=[
            InputRequired(),
        ],
    )
    referee2 = StringField(
        'Referee 2 (not required for Student Applications, enter "None")',
        validators=[
            InputRequired(),
        ],
    )
