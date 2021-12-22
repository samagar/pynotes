# views.py
'''
Main py component with all functions in it to view main page, add, update and delete records.
Login and logout functionalities
'''

# System Module Imports
from flask import Flask, render_template, request, session, \
     flash, redirect, url_for, g, jsonify

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from functools	import wraps
import datetime

# Custom Module imports 
from models import Notes, db
from forms import AddNoteForm, RegisterForm, LoginForm
app = Flask(__name__)
app.config.from_object('_config')
db.init_app(app)
db.app = app

# login required function
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))
	return wrap	

# login function
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
			session.pop('_flashes', None)
			return redirect(url_for('main'))
	return render_template('login.html', error=error), status_code

# logout function
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out')
	return redirect(url_for('login'))

# main landing page
@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
	user = 1
	callfrom = request.args.get('callfrom')

	if callfrom == 'select':
		note_id = request.args.get('note_id')
		notes = db.session.query(Notes) \
		.filter_by(user_id=user, note_id=note_id).order_by(Notes.note_id.desc())
		for p in notes:
			title=p.title
			detail=p.detail
			break
		return jsonify({'title':title, 'detail':detail, note_id:note_id})
	elif callfrom == 'new':
		title = ''
		detail = ''
		note_id = None
		return jsonify({'title':title, 'detail':detail, 'note_id':note_id})
	else:
		notes = db.session.query(Notes) \
		.filter_by(user_id=user).order_by(Notes.note_id.desc())
		for p in notes:
			title = p.title
			detail = p.detail
			note_id = p.note_id
			break
		return render_template('main.html',note_id=note_id, notes=notes, title=title, detail=detail)


# Item Update
@app.route("/update", methods=['GET', 'POST'])
@login_required
def update():
	# user = session['username']
	user = 1
	title = request.form['title']
	detail = request.form['detail']
	note_id = request.form['note_id']

	db.session.query(Notes).filter_by(note_id=note_id).update({"title": title, "detail": detail})
	db.session.commit()
	return jsonify({'var': 'test'})

# Item Select
@app.route("/select", methods=['GET'])
@login_required
def select():
	note_id = request.args.get('note_id')
	return redirect(url_for('main', note_id=note_id, callfrom="select"))

# Item Add
@app.route('/add',methods=['POST'])
@login_required
def add():
	form = AddNoteForm(request.form)	
	if request.method == 'POST':
#		if form.validate_on_submit():
		new_task = Notes(form.title.data,
		form.detail.data,1,
		"10/12/2016",
#			datetime.datetime.utcnow(),
		"1")
		db.session.add(new_task)
		db.session.commit()
		return jsonify({'var1': "Entry added"})
	return redirect(url_for('main'))

# Item Delete
@app.route('/delete',methods=['POST'])
@login_required
def delete():
	note_id = request.form['note_id']
	db.session.query(Notes).filter_by(note_id=note_id).delete()
	db.session.commit()
	return jsonify({ 'var1': "Entry deleted"})	