from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField, PasswordField, DateField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from uzenofal.models import User

class NewObjectForm(FlaskForm):
    title = StringField("Áru neve", validators=[DataRequired()])
    price = IntegerField("Ár", validators=[DataRequired()])
    date = DateField('Rögzítés dátuma', validators=[DataRequired()])
    submit = SubmitField('Mentés')

class NewUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Nem megfelelő e-mail cím!')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField('Password again', validators=[DataRequired(), 
                                                                         EqualTo('password',
                                                                                 message='Nem egyezik meg a fent megadott jelszóval')])

    submit1 = SubmitField('Regisztráció')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ez a felhasználónév már foglalt. Adjon meg másikat!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ez az e-mail cím már foglalt. Adjon meg másikat!')
    
    