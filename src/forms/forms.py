from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models import User, Company
from itertools import cycle

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),
                            Length(min = 2, max = 20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password =PasswordField('Confirm Password',
                            validators = [DataRequired(), EqualTo('password')])
    register = SubmitField('Registrarme')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    login = SubmitField('Iniciar sesion')

class CompanyForm(FlaskForm):
    name = StringField('name', validators = [DataRequired(), Length(max = 20)])
    rut = StringField('rut', validators = [DataRequired(), Length(max = 20)])
    submit = SubmitField('Crear empresa')

    def validate_rut(self, rut):
        aux = rut.data.upper().replace(".","")[:-2];
        dv = rut.data[-1]
    
        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11
        if str(res) == dv:
            return True
        elif dv=="K" and res==10:
            return True
        else:
            raise ValidationError('Este RUT no es valido. Por favor ingresa otro RUT.')

class ContactForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    subject = StringField('Asunto', validators = [DataRequired(),
                            Length(min = 0, max = 150)])
    body = TextAreaField('Escribe tu mensaje aquí...', validators = [DataRequired()])
    submit = SubmitField('Enviar mensaje')

