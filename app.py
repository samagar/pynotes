# Import db and flask components
import sqlite3
from flask import Flask, render_template, flash, session, \
redirect, url_for, request, g

# Import wraps to enable execute mandatory models before 
# any fucntion to avoid unauth acess
from functools import wraps

# Crete App object and import config
app = Flask(__name__)
app.config.from_object('_config')

# Connect db
def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

# Login function
def login_required(test):
    @wraps(test)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return test(*args,**kwargs)
        else:
            flash('you need to login first')
            return redirect(url_for('login'))
    return wrap

@app.route("/main",methods=['GET','POST'])
@login_required
def main():
    db = connect_db()
    curr = db.execute('select * from Notes')
    notes = [dict(note_id=row[0],title=row[1],detail=row[2]) for row in curr.fetchall()]
    db.close()

    title = notes[-1]['title']
    detail = notes[-1]['detail']
    note_id = notes[-1]['note_id']

    callfrom = request.args.get('callfrom')

    if callfrom == 'display':
        title = request.args.get('title')
        detail = request.args.get('detail')
        note_id = request.args.get('note_id')
    elif callfrom == 'new':
        title = '' 
        detail = ''
        note_id = None

    return render_template('main.html',note_id=note_id, notes=notes, title=title, detail=detail)

@app.route('/',methods=['GET','POST'])
def login():
    error  = None
    status_code = 201

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            flash('incorrect credentials..try again')
            status_code = 401
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return redirect(url_for('main'))
    return render_template('login.html', error = error), status_code


@app.route('/add',methods=['POST'])
@login_required
def notes():

    title = request.form['title']
    detail = request.form['detail']
    requesttype = request.form['savedata']
    user = session["username"]
    note_id = request.args.get('note_id')

    if requesttype == 'Update':
        g.db = connect_db()
        curr = g.db.execute("UPDATE Notes  \
            set title = ?, detail =?, posted_date = '10/16/2021' where note_id =?",(title, detail, note_id))
        g.db.commit()
        g.db.close()
        flash('Entry Updated')
        return redirect(url_for('main', title=title, detail=detail, callfrom='display', note_id=note_id))
    
    if requesttype == "Save":
        if not title or not detail:
            flash('You need to enter all fields')
            return redirect(url_for('main', callfrom='new'))

        g.db = connect_db()
        curr = g.db.execute('INSERT INTO Notes(title, detail, posted_date, Userid, status) \
        values (?,?,?,?,?)', 
        [request.form['title'],request.form['detail'],"10/16/2021",user,1])
        g.db.commit()
        g.db.close()
        flash('new entry added')

    if requesttype == "Delete":
        g.db = connect_db()
        g.db.execute('delete from notes where note_id='+str(note_id))
        g.db.commit()
        g.db.close()
        flash('The note was deleted.')
    
    return redirect(url_for('main'))

@app.route('/logout')
@login_required
def log_out():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# Delete Tasks
@app.route('/delete/<int:note_id>')
@login_required
def delete_entry(note_id):
    g.db = connect_db()
    g.db.execute('delete from notes where note_id='+str(note_id))
    g.db.commit()
    g.db.close()

    flash('The note was deleted.')
    return redirect(url_for('main'))

# Display Notes
@app.route('/display/<int:note_id>')
@login_required
def display_entry(note_id):
    g.db = connect_db()
    row = g.db.execute('select * from notes where note_id='+str(note_id)).fetchone()
    note_row = dict(note_id=row[0],title=row[1],detail=row[2]) 
    g.db.close()
    return redirect(url_for('main', code=307, title=note_row['title'], detail=note_row['detail'], callfrom='display', note_id=note_id))
    
if __name__ == '__main__':
    app.run(host='localhost', port='8000', debug=True)

    #                     <a href="{{ url_for('delete_entry', note_id=note_id) }}"><button class="oth-btn">Delete</button></a>
    
