from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField, PasswordField, DateField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from uzenofal.models import User

class NewObjectForm(FlaskForm):
    title = StringField(label="Áru neve", validators=[DataRequired()])
    price = IntegerField(label="Ár", validators=[DataRequired()])
    date = DateField(label='Rögzítés dátuma', validators=[DataRequired()])
    submit = SubmitField(label='Mentés')

class NewUserForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=3,max=10)])
    email = StringField(label='E-mail', validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label='Password again', validators=[DataRequired(), 
                                                                         EqualTo('password',
                                                                                 message='nem egyezik meg a fent megadott jelszóval')])

    submit = SubmitField(label='Regisztráció')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ez a felhasználónév már foglalt. Adjon meg másikat!')
