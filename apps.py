
# imports
import sqlite3

from flask import Flask, render_template, request, session, \
     flash, redirect, url_for, g

from functools	import wraps

app = Flask(__name__)
# Pulls in app config by looking in uppercase variables
app.config.from_object('_config')
# app.config.from_object(__name__)

# Function to connect to Db
def connect_db():
	return sqlite3.connect(app.config["DATABASE"])

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
	g.db = connect_db()
	curr = g.db.execute('select * from notes')
	posts = [dict(title=row[0], detail=row[1]) for row in curr.fetchall()]
	g.db.close()
	return render_template("main.html", posts=posts)


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


@app.route('/add', methods=['POST'])
@login_required
def add():
	title = request.form['title']
	post = request.form['post']
	if not title or not post:
		flash("All fields required..try again")
		return(url_for('main'))
	else:
		g.db = connect_db()
		cur = g.db.execute('insert into posts (title, post) values (?,?)',[request.form['title'], request.form['post']])
		g.db.commit()
		g.db.close()
		flash("new entry added")
		return redirect(url_for('main'))

	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out')
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)

