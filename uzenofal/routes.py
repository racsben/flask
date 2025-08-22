from flask import Flask, redirect, url_for, render_template, request, flash

from uzenofal import app, db, bcrypt
from uzenofal.models import Object, User
from uzenofal.data import test_aruk, test_users
from uzenofal.forms import NewObjectForm, NewUserForm

with app.app_context():
    db.create_all()
    for user in test_users:
        hashed_pswd = bcrypt.generate_password_hash('alma24').decode('utf-8') 
        user_obj = User(username=user['username'], email=user['email'], password=hashed_pswd)
        db.session.add(user_obj)
    for aru in test_aruk:
        aruk_obj = Object(title=aru['title'], price=aru['price'], user_id=aru['user_id'], date=aru['date'])
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
            current_aru = Object(title=form.title.data, price=form.price.data, date=form.date.data)
            db.session.add(current_aru)
            db.session.commit()
            flash('Az áru feltöltésre került! :)', 'success')     
            return redirect(url_for('kezdolap'))
    return render_template('create.html', title="Új áru", form=form) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_user_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_user_pswd)
            db.session.add(user)
            db.session.commit()
            flash('Sikeres regisztráció. Jelentkezz be!', 'success')     
            print(User.query.all())
            return redirect(url_for('kezdolap'))
    return render_template('register.html', title="Regisztráció", form=form) 


