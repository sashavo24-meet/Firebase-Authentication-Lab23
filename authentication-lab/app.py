from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
      "apiKey": "AIzaSyA_mnC2-wPq1X-7Co8tILmw5m5jDdYiYHo",
  'authDomain': "evian-9241f.firebaseapp.com",
  'projectId': "evian-9241f",
  'storageBucket': "evian-9241f.appspot.com",
  'messagingSenderId': "718261099089",
  'appId': "1:718261099089:web:a988a4eb4facd26bc07670",
  'measurementId': "G-T6Y85L2BV5",
  "databaseURL": "https://evian-9241f-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'GET':
        email = request.form["Email"]
        password = request.form["Password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "failed to login"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'GET':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "failed to signup"
    return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)