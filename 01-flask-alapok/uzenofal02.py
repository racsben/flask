from flask import Flask, redirect, url_for, render_template, request, flash
from data import aruk
from forms import NewObjectForm
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '668c2abe469d88c75a881d0170c5d98a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=True)


with app.app_context():
    db.create_all()
    for aru in aruk:
        aruk_obj = Object(title=aru['title'], price=aru['price'])
        db.session.add(aruk_obj) 
    db.session.commit()
    print(Object.query.all())


@app.route("/")
@app.route("/kezdolap")
def kezdolap():
    return render_template('index.html', title="Kezdőlap")

@app.route("/galeria")
def galeria():
    aruk_db = db.session.execute(db.select(Object)).scalars()
    return render_template('gallery.html', aruk=aruk_db, title="Galéria")

@app.route("/kapcsolat")
def kapcsolat():
    return render_template('contact.html', title="Kapcsolat")

@app.route("/rolam")
def rolam():
    return render_template('about.html', title="Rólam")

@app.route('/create/new', methods=['GET', 'POST'])
def create():
    form = NewObjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_aru = Object(title= form.title.data, price= form.price.data)
            db.session.add(current_aru)
            db.session.commit()
            flash('Az áru feltöltésre került! :)', 'success')     
            return redirect(url_for('kezdolap'))
    return render_template('create.html', title="Új áru", form=form) 


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) #Hogy újrainduljon magátol 