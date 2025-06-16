from flask import Flask, render_template, request, Response, redirect, url_for, flash
from config import Config
from werkzeug.utils import secure_filename
import sqlite3
import random
import os

app=Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Allows configuration like settings to be tucked away in a separate file.  See config.py
app.config.from_object(Config)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
@app.route('/teddy/<int:id>', methods=['GET', 'POST'])
def teddy_details(id):
  # print("The teddy id is {}".format(id))  # DEBUG
  conn = get_db_connection()
  
  if request.method == 'POST':
    # Handle form submission here if needed
    # For example, you could update the teddy's information or delete it
    # This is just a placeholder for now
    return "Form submitted successfully", 200
  else:
    
    
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


@app.route('/pictures')
def index():
    """Display the upload form."""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    # Check if file was submitted
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if file was actually selected
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    # Validate and save file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Add timestamp to filename to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        flash(f'File "{filename}" uploaded successfully!')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, WebP)')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/contact-us')
def contact_us():
  message = ""
  if len(request.args) > 0:
    message = "This message is returned to the form page"
        
    name = request.args.get('name')
    comment = request.args.get('comment')
    
  return render_template('contact.html', message=message)


if __name__ == '__main__':
  app.run(debug=app.config['DEBUG'], port=8080, host='0.0.0.0') 