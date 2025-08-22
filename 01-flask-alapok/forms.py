from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired, Length

class NewObjectForm(FlaskForm):
    title = StringField(label="Áru neve", validators=[DataRequired()])
    price = IntegerField(label="Ár", validators=[DataRequired()])
    submit = SubmitField(label='Mentés')