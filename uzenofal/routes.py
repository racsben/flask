from flask import Flask, redirect, url_for, render_template, request, flash, abort
from flask_login import login_user, current_user, login_required, logout_user

from uzenofal import app, db, bcrypt
from uzenofal.models import Object, User
from uzenofal.data import test_aruk, test_users
from uzenofal.forms import NewObjectForm, NewUserForm, LoginForm

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

@app.route("/card/<int:object_id>")
def card(object_id):
    current_obj = Object.query.get_or_404(object_id)
    return render_template('card.html', title=current_obj.title, object=current_obj)

@app.route('/create/new', methods=['GET', 'POST'])
@login_required
def create():
    form = NewObjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_aru = Object(title=form.title.data,user_id=current_user.get_id(), price=form.price.data, date=form.date.data)
            db.session.add(current_aru)
            db.session.commit()
            flash('Az áru feltöltésre került! :)', 'success')     
            return redirect(url_for('galeria'))
    return render_template('create.html', title="Új áru", form=form) 

@app.route('/object/<int:object_id>/update', methods=['GET', 'POST'])
@login_required
def update_object(object_id):
    current_obj = Object.query.get_or_404(object_id)
    if current_obj.feltolto != current_user:
        abort(403)
    form = NewObjectForm()
    if form.validate_on_submit():
        current_obj.title = form.title.data
        current_obj.price = form.price.data
        current_obj.date = form.date.data
        db.session.commit()
        flash('A kurzus adatai frissítésre kerültek', 'succes')
        return redirect(url_for('card', object_id=current_obj.id))
    elif request.method == 'GET':
        form.title.data = current_obj.title
        form.price.data = current_obj.price
        form.date.data = current_obj.date
    return render_template('create.html', title="Kurzus frissítése", form=form, legend='Kurzus adatainak frissítése')    

@app.route('/object/<int:object_id>/delete', methods=['POST'])
@login_required
def delete_object(object_id):
    current_obj = Object.query.get_or_404(object_id)
    if current_obj.feltolto != current_user:
        abort(403)
    db.session.delete(current_obj)
    db.session.commit()
    flash('A kurzus törlésre került', 'succes')
    return redirect(url_for('galeria'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = NewUserForm()
    if form.validate_on_submit():
        hashed_user_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_user_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Sikeres regisztráció. Jelentkezz be!', 'success')     
        print(User.query.all())
        return redirect(url_for('kezdolap'))
    return render_template('register.html', title="Regisztráció", form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('kezdolap'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Sikeres bejelentkezés')
            return redirect(next_page) if next_page else redirect(url_for('kezdolap'))
        else:
            flash('Sikertelen bejelentkezés. Ellenőrizd az email címet és jelszót!', 'danger')
    return render_template('login.html', title="Bejelentkezés", form=form) 


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('kezdolap'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Felhasználói fiók')
