from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from werkzeug.security import check_password_hash

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        user = g.session.query(User).filter_by(username=username.data).first()
        self.hash = user.password if user else None

    def validate_password(self, password):
        if not self.hash or not check_password_hash(self.hash, password.data):
            raise ValidationError('Invalid Username or Password')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()]) 
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = g.session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

