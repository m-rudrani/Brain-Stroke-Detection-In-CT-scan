import os
from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import numpy as np
from keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
import cv2
from io import BytesIO
from PIL import Image
import base64

app = Flask(__name__)

# Set the path to the local folder to save uploaded images
UPLOAD_FOLDER = 'static/uploaded_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dic = {0: 'hemorrhagic Brain Stroke', 1: 'ischaemic Brain Stroke ', 2:'normal'}

# Configure SQLite database
DATABASE = 'database.db'

def create_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT,
                  email TEXT, 
                  mobile INTEGER, 
                  username TEXT UNIQUE, 
                  password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT ,
                  label TEXT,
                  image_data BLOB,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()


# def insert_admin(name, email, mobile, username, password):
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     sql_query = "INSERT INTO users (name, email, mobile, username, password) VALUES (?, ?, ?, ?, ?)"
#     params = (name, email, mobile, username, password)
#     c.execute(sql_query, params)
#     conn.commit()
#     conn.close()

# insert_admin("Admin", "admin@example.com", 1234567890, "admin", "admin")

def insert_user(name, email, mobile, username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    sql_query = "INSERT INTO users (name, email, mobile, username, password) VALUES (?, ?, ?, ?, ?)"
    params = (name, email, mobile, username, password)
    c.execute(sql_query, params)
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def insert_prediction(user_id, label, image_path):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # sql_query = "INSERT INTO predictions (user_id, label, image_data) VALUES (?, ?, ?)"
    # params = (user_id, label, image_data)
    c.execute("INSERT INTO predictions (user_id, label, image_data) VALUES (?, ?, ?)",(user_id, label, image_path))
    conn.commit()
    conn.close()

@app.route("/")
def homepage():
    return render_template('landing.html')

@app.route("/home")
def home():
    if 'username' in session and session['username'] == 'admin':
        return redirect(url_for('landing_admin'))
    else:
        return render_template('index.html')

@app.route("/landing")
def landing():
    return render_template('landing.html')

img_size_x = 256
img_size_y = 256
model = load_model('model.h5')

def predict_label(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    resized = cv2.resize(gray, (img_size_x, img_size_y)) 
    i = img_to_array(resized) / 255.0
    i = i.reshape(1, img_size_x, img_size_y, 1)
    predict_x = model.predict(i) 
    p = np.argmax(predict_x, axis=1)
    return dic[p[0]]

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    p = None
    photo = None
    img_path = None

    if request.method == "POST" and 'photo' in request.files:
        # Get the uploaded file from the form data
        photo = request.files['photo']
        
        if photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
            img_path=photo_path 


            # Perform prediction
            p = predict_label(img_path)

            # Get user_id from session (assuming user_id is stored in session)
            user_id = session.get('username')

        
            img = cv2.imread(img_path)
            # Save prediction to database

            # Save prediction to database
            insert_prediction(user_id,p,img)
            
         
    cp = str(p).lower() if p is not None else ""
    src = img_path if img_path is not None else ""

    return render_template('upload.html', cp=cp, src=src)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name'] 
        email = request.form['email']
        mobile = request.form['mobile']
        username = request.form['username']
        password = request.form['password']
        
        if get_user(username):
            message = "User already exists!"
            return render_template('signup.html', message=message)
        insert_user(name, email, mobile, username, password)
        message = "Account successfully created"
        return render_template('signup.html', message=message)
    return render_template('signup.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)

        if user and user[5] == password:
            session['username'] = username
            session['user_id'] = user 
            # Check if the user is an admin
            if username == 'admin':
                return redirect(url_for('landing_admin'))
            else:
                return redirect(url_for('home'))
        return render_template('login.html', message="Invalid username or password!")
    return render_template('login.html')


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('landing'))

@app.route("/landing_admin")
def landing_admin():
    return render_template('landing_admin.html')

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))

    if request.method == "POST":
        # Handle user removal
        username_to_remove = request.form.get('username')
        # Call a function to remove the user from the database
        remove_user(username_to_remove)
        return redirect(url_for('admin'))

    # Fetch all users from the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT name, email, mobile, username FROM users")
    users = c.fetchall()

    # Fetch prediction data for each user
    user_predictions = {}
    for user in users:
        username = user[3]
        c.execute("SELECT * FROM predictions WHERE user_id=?", (username,))
        predictions = c.fetchall()
        if predictions:  # Check if predictions exist
            user_predictions[username] = predictions
        else:
            user_predictions[username] = []
    conn.close()

    return render_template('admin.html', users=users, user_predictions=user_predictions)

def remove_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # Create the database if it doesn't exist
    if not os.path.exists(DATABASE):
        create_db()
    
    # Secret key for session management
    app.secret_key = 'supersecretkey'
    
    app.run(debug=True)
