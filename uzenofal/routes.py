from flask import Flask, redirect, url_for, render_template, request, flash

from uzenofal import app, db
from uzenofal.models import Object
from uzenofal.data import aruk
from uzenofal.forms import NewObjectForm

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

