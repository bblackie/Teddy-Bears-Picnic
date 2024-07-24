from flask import Flask, render_template, request
from config import Config
import sqlite3
import random

app=Flask(__name__)
app.config.from_object(Config)


# Get the title of the website from Config and
# make it available to all templates. Used in
# header.html and layout.html in this case
@app.context_processor
def context_processor():
  return dict(title=app.config['TITLE'])


# The home page
@app.route('/')
def home():
  return render_template('home.html')


# Displays all teddys in the database
# TODO: link each teddy to its own details page
@app.route('/all_teddys')
def all_teddys():
    # This boilerplate db connection could (should?) be in
    # a function for easy re-use
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM Teddy ORDER BY id;")
    # fetchall returns a list of results
    teddys = cur.fetchall()
    conn.close()  # always close the db when you're done.
    # print(teddys)  # DEBUG
    return render_template("all_teddys.html", teddys=teddys)


# Individual teddy details page.
@app.route('/teddy/<int:id>')
def teddy_details(id):
  # print("The teddy id is {}".format(id))  # DEBUG
  conn = sqlite3.connect(app.config['DATABASE'])
  cur = conn.cursor()
  cur.execute("SELECT * FROM Teddy WHERE id=?;",(id,))
  # fetchone returns a tuple containing the data for one entry
  teddy = cur.fetchone()
  conn.close()
  return render_template("teddy.html", teddy=teddy)


# about Teddy Bears Picnic
@app.route('/about')
def about():
  formstuff = None
  if len(request.args) > 0:
    formstuff = []
    formstuff.append(request.args.get('username'))
    formstuff.append(request.args.get('password'))
  return render_template('about.html', formstuff=formstuff)


if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], port=8080, host='0.0.0.0') 