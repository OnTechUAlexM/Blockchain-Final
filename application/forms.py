from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FloatField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flask_login import current_user
from .models import db, Wallet, Vehicle


class CostField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid number. Cannot denote larger numbers with commas.'))


class SignupForm(FlaskForm):
    """Signup Form"""
    email = StringField(
        '* Email',
        validators=[
            Length(min=6),
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        '* Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Your password must be at least 8 characters long.')
        ]
    )
    confirm = PasswordField(
        '* Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords do not match.')
        ]
    )

    # Recaptchas will work given that RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY
    # are filled in using a google key, which can be acquired here:
    # https://developers.google.com/recaptcha/docs/display
    # recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class AddVehicleForm(FlaskForm):
    """ Create a transaction Form """
    vin = StringField(
        'VIN',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    make = StringField(
        'Make',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    model = StringField(
        'Model',
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )
    year = StringField(
        'Year',
        validators=[
            DataRequired(),
            Length(min=4, max=5)
        ]
    )
    condition = StringField(
        'Condition',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    mileage = FloatField(
        'Mileage',
        validators=[
            InputRequired()
        ]
    )
    cost = CostField(
        'Cost $',
        validators=[
            InputRequired()
        ]
    )


class ConfirmPurchaseForm(FlaskForm):
    vid = HiddenField(
        'vid',
        validators=[
            DataRequired()
        ]
    )

    def validate_vid(form, field):
        w = Wallet.query.filter_by(uid=current_user.id).first()
        v = Vehicle.query.filter_by(id=int(field.data)).first()
        if w.amt < v.cost:
            raise ValidationError("You do not have enough funds to purchase this vehicle")
        w.amt = w.amt - v.cost
        db.session.commit()




