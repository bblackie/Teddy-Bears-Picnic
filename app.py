from flask import Flask, render_template, request, Response
from config import Config
import sqlite3
import random

app=Flask(__name__)


# Allows configuration like settings to be tucked away in a separate file.  See config.py
app.config.from_object(Config)



def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

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
@app.route('/teddys')
def all_teddys():
    # This boilerplate db connection could (should?) be in
    # a function for easy re-use
    conn = get_db_connection()
    
    # fetchall returns a list of results
    teddys = conn.execute("SELECT * FROM Teddy ORDER BY name;").fetchall()
    conn.close()  # always close the db when you're done.
    # print(teddys)  # DEBUG
    return render_template("all_teddys.html", teddys=teddys)


# Individual teddy details page.
@app.route('/teddy/<int:id>')
def teddy_details(id):
  # print("The teddy id is {}".format(id))  # DEBUG
  conn = get_db_connection()
  
  # You might be asking yourself why you couldn't write a query like: cur.execute(f"SELECT * FROM Teddy WHERE id={id};") 
  # Simply put, this is insecure and allows for SQL injection.  For example, if someone set variable id="2; DROP TABLE *;" then the table gets deleted.
  # Instead, it's better to use the id=? and to provide the parameter as a separate tuple.  "(id,)" looks weird but it's simply a tuple (collection) with one value.
  teddy = conn.execute("SELECT * FROM Teddy WHERE id=?;",(id,)).fetchone()
  # fetchone returns a tuple containing the data for one entry
  if teddy is None:
    return render_template("404.html"), 404  # Return a 404 error if teddy not found
  conn.close()
  return render_template("teddy.html", teddy=teddy, another_variable="Another value", and_another=8)


# about Teddy Bears Picnic
@app.route('/about')
def about():
  formstuff = None
  if len(request.args) > 0:
    formstuff = []
    formstuff.append(request.args.get('username'))
    formstuff.append(request.args.get('password'))
  return render_template('about.html', formstuff=formstuff)

# Displays a random teddy bear from the database
@app.route('/image/<int:image_id>')
def get_image(image_id):
    # Fetch image data from database
    conn = get_db_connection()
  

    image_data = conn.execute("SELECT img_blob FROM Teddy WHERE id = ?",(image_id,)).fetchone()
    conn.close()
    if image_data is None:
        return "Image not found", 404
    image_data = image_data['img_blob']
    if image_data is None:
        return "Image data is empty", 404
    # Assuming image_data is in bytes format
    if not isinstance(image_data, bytes):
        return "Invalid image data", 500
    # Return the image data as a response
    
    return Response(image_data, mimetype='image/jpeg')  # or appropriate MIME type


if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], port=8080, host='0.0.0.0') 