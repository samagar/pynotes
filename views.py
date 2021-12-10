# views.py

from flask import Flask, render_template, request, session, \
     flash, redirect, url_for, g, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools	import wraps
import datetime

# Import Model Db
from models import Notes, db

# Import Form
from forms import AddNoteForm, RegisterForm, LoginForm

# Pulls in app config by looking in uppercase variables
app = Flask(__name__)
app.config.from_object('_config')
db.init_app(app)
db.app = app

# = SQLAlchemy(app)

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))
	return wrap	

@app.route("/main")
@login_required
def main():
	user = session["username"]
	user = 1
	notes = db.session.query(Notes) \
			.filter_by(user_id=user).order_by(Notes.posted_date.asc())
	callfrom = request.args.get('callfrom')
	if callfrom == 'display':
		title = request.args.get('title')
		detail = request.args.get('detail')
		note_id = request.args.get('note_id')
		return render_template('main.html',note_id=note_id, notes=notes, title=title, detail=detail)
	elif callfrom == 'new':
		title = '' 
		detail = ''
		note_id = None
		return render_template('main.html',note_id=note_id, notes=notes, title=title, detail=detail)
	else:
		return render_template("main.html", notes=notes)
	

@app.route("/", methods=['GET', 'POST'])
def login():
	error = None
	status_code = 202
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or \
					request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid credentials, please try again'
			status_code = 401			
		else:
			session['logged_in'] = True
			return redirect(url_for('main'))
	return render_template('login.html', error=error), status_code


@app.route('/add',methods=['POST'])
@login_required
def notes():
	title = request.form['title']
	requesttype = request.form['requesttype']
	detail = request.form['detail']
	user = session['username']
	form = AddNoteForm(request.form)

	if requesttype == "Update":
		note_id = request.form['note_id']
		db.session.query(Notes).filter_by(note_id=note_id).update({"title": title, "detail": detail})
		db.session.commit()
		return jsonify({ 'var1': "Entry Updated"})

	if requesttype == "Save":
		if request.method == 'POST':
#			if form.validate_on_submit():
			new_task = Notes(form.title.data,
			form.detail.data,1,
			"10/12/2016",
#			datetime.datetime.utcnow(),
			"1")
			db.session.add(new_task)
			db.session.commit()
			return jsonify({'var1': "Entry added"})
		return redirect(url_for('main'))

	if requesttype == "Delete":
		note_id = request.form['note_id']
		db.session.query(Notes).filter_by(note_id=note_id).delete()
		db.session.commit()
		return jsonify({ 'var1': "Entry deleted"})	

# Display Notes
@app.route('/display/<int:note_id>')
@login_required
def display_entry(note_id):
	user = 1
	notes = db.session.query(Notes) \
		.filter_by(user_id=user, note_id=note_id).order_by(Notes.posted_date.asc())
	for p in notes:
		title=p.title
		detail=p.detail

	return redirect(url_for('main', code=307, title=title, 
		detail=detail, callfrom='display',note_id=note_id))


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out')
	return redirect(url_for('login'))