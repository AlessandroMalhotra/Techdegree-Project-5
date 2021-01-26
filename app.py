from flask import Flask, g, render_template, flash, redirect, url_for, request
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

import forms
import models

app = Flask(__name__)
app.secret_key = 'ajjdvdkjvfkjvkfvdhgxsydgsbcyvuvnvvn!'

login_manager = LoginManager()
login_manager.init_app(app)
Login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterationForm()
    if form.validate_on_submit():
        flash('Yay, you registered','success')
        models.User.generate_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
       try:
           user = models.User.get(models.User.email == form.email.data)
       except models.DoesNotExist:
            flash("Your email or password doesn't match", "error")
       else:
           if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
           else:
               flash("Your email or password doesn't match", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!, Come back soon!', 'success')
    return redirect(url_for('index'))

@app.route('/entries')
def index():
    entries = models.Add.select().limit(100)
    return render_template('index.html', entries=entries)



@app.route('/entries/new', methods=('GET', 'POST'))
@login_required
def new_entry():
    form = forms.AddForm()
    if form.validate_on_submit():
        models.Add.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.date.data,
            learned=form.learning.data.strip(),
            resources=form.resources.data.strip(),
        ).save()
        flash('Journal Added! Thanks!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def detail_entry(id):
    entry = models.Add.get(models.Add.id == id)


@app.route('entries/<int:id>/edit')
@login_required
def edit_entry():
     entry = models.Add.get(models.Add.id == id)
     form = forms.AddForm()
     if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.resources = form.resources.data
        entry.save()
        flash('Journal edited!', 'success')
        return redirect(url_for('index'))
     return render_template('edit.html', entry=entry, form=form, id=id)   


@app.route('/entries/<int:id>/deletecheck')
@login_required
def deletecheck(id):
    entry = models.Entry.get(models.Entry.id == id)
    return render_template('delete.html', entry=entry)

@app.route('entries/<int:id>/delete')
def delete_entry():
    entry = models.Entry.get(models.Entry.id == id)
    entry.delete_instance()
    flash('Entry deleted.', 'success')
    return redirect(url_for('index'))




if __name__ == '__main__':
    models.initialize()
    try:
        models.User.generate_user(
            username='alessandro',
            email='alessandro244@outlook.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)