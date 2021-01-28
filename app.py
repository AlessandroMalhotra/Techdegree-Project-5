from flask import Flask, g, render_template, flash, redirect, url_for, request

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

import forms
import models

app = Flask(__name__)
app.secret_key = 'ajjdvdkjvfkjvkfvdhgxsydgsbcyvuvnvvn!'


@app.before_request
def before_request():
    """Connects Database"""
    g.db = models.DATABASE
    g.db.connect()
    

@app.after_request
def after_request(response):
    """Closes the Database"""
    g.db.close()
    return response

@app.route('/')
@app.route('/entries')
def index():
    """Main Paige with Entries"""
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)



@app.route('/entries/new', methods=('GET', 'POST'))
def new_entry():
    """ Adds a entry """
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
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
    try:
        entry = models.Entry.get(models.Entry.entry_id == id)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def edit_entry():
     try:
        entry = models.Entry.get(models.Add.id == id)
     except models.DoesNotExist:
         abort(404)
     
     form = forms.EntryForm()
     if form.validate_on_submit():
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time_spent = form.time_spent.data
        entry.learned = form.learned.data
        entry.resources = form.resources.data
        entry.save()
        flash('Journal edited!', 'success')
        return redirect(url_for('index'))
     return render_template('edit.html', entry=entry, form=form)   



@app.route('/entries/<int:id>/delete')
def delete_entry():
    try:
        entry = models.Entry.get(models.Entry.entry_id == id)
        entry.delete_instance()
        flash('Entry deleted.', 'success')
    except models.DoesNotExist:
        abort(404)
    return redirect(url_for('index'))


@app.errorhandler(404)
def error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)