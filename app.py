from flask import Flask, request, render_template,redirect,url_for,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

import uuid  # For generating unique tokens
import smtplib  # For sending emails
from email.mime.text import MIMEText  # For composing email content
from email.mime.multipart import MIMEMultipart  # For composing email content

import numpy as np
import pandas
import sklearn
import pickle
import warnings

''' 
{%...%} condations, for loops
{{   }} expressions to print output
{#...#} this is for comments
'''

warnings.filterwarnings("ignore", category=DeprecationWarning)

model = pickle.load(open('models/RandomForest.pkl','rb'))

app = Flask(__name__)
app.secret_key = "4949skjdjfdjfjfkfkksd"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

#User Loader funcation
@login_manager.user_loader
def load_user(email):
    return User.get(email)

class User(UserMixin):
    def __init__(self, user_id,name, email):
        self.id = user_id
        self.name = name
        self.email = email
     
       
 

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute('select name, email from users where id = %s',(user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(user_id, result[0],result[1])




@app.route('/') # THis is decoreater its use for create a url.
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/features.html')
def features():
    return render_template('features.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
       
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('select id,name,email, password from users where email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data and bcrypt.check_password_hash(user_data[3], password):
            user = User(user_data[0],user_data[1],user_data[2])
            login_user(user)
            flash('login successfully insert the data and predict the crop', 'success')
            return render_template('crop.html')

        else:
            flash('Invalid email or password. Please try again.', 'error')

      
    return render_template('login.html')



@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
       
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE email = %s', (email,))
        count = cursor.fetchone()[0]
        cursor.close()
        if count > 0:
            flash('Email already taken. Please choose a different email.', 'error')
            return redirect(url_for('signup'))
    

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute('insert into users (name,email,password) values(%s,%s,%s)',(name,email,hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash('Account created successfully. You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route("/predict",methods=['POST'])
@login_required
def predict():

    N = request.form['Nitrogen']
    P = request.form['Phosporus']
    k = request.form['Potassium']
    temperature = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    feature_list = [N,P,k,temperature,humidity,ph,rainfall]
    features = np.array([[feature_list]]).reshape(1, -1)
    prediction = model.predict(features)[0]

    if True:

       result = "{} is a best crop to be cultivated. ".format(prediction)

    return render_template('crop.html',result = result)
   


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout successful see you soon.', 'success')
    return redirect(url_for('index'))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # Check if the email exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id FROM users WHERE email = %s', (email,))
        user_id = cursor.fetchone()
        cursor.close()

        if user_id:
            # Generate a unique token for password reset
            token = str(uuid.uuid4())

            # Save the token in the database
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET reset_token = %s WHERE id = %s', (token, user_id[0]))
            mysql.connection.commit()
            cursor.close()

            # Send email with password reset link
            send_reset_email(email, token)
            flash('Password reset instructions have been sent to your email.', 'success')
        else:
            flash('Email address not found. Please try again.', 'error')

    return render_template('forgot_password.html')

def send_reset_email(email, token):
    # Email sending logic goes here
    # Example using SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'subhoy2370@gmail.com'
    sender_password = 'zytp ymro kshi kyxx'
    receiver_email = email

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Password Reset Request'

    body = f"""
    To reset your password, click the following link:
    http://localhost:5000/reset_password?token={token}
    """

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        # Extract the token and new password from the form submission
        token = request.form['token']
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validate the new password and confirm password match
        if new_password != confirm_password:
            return "Passwords do not match. Please try again."
        # Verify the token and update the user's password in the database
        else:
           cursor = mysql.connection.cursor()
           cursor.execute('SELECT id FROM users WHERE reset_token = %s', (token,))
           user = cursor.fetchone()
           cursor.close()

        if user:
            # Hash the new password
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

            # Update the user's password and clear the reset token
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET password = %s, reset_token = NULL WHERE id = %s', (hashed_password, user[0]))
            mysql.connection.commit()
            cursor.close()

            flash("Password reset successful. You can now login with your new password.", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid or expired token. Please request a new password reset.", "error")
            return redirect(url_for('forgot_password'))

        # TODO: Verify the token and update the user's password in the database
        # Implement your logic to verify the token and update the user's password
        
     


    # If the request method is GET, render the reset_password.html template
    # Pass the token value from the URL query parameters to the template
    token = request.args.get('token')
    return render_template('reset_password.html', token=token)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login'))

if __name__ == "__main__":
            app.run(debug=True)