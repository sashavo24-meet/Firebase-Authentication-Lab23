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
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'email': email, 'password': password, 'name': full_name, 'username': username, 'bio': bio}
            db.child('Users').child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "failed to signup"
    return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        Title = request.form['Title']
        Text = request.form['Text']
        try:
            UID = login_session['user']['localId']
            tweet = {'Title': Title, 'Text': Text, 'UID': UID}
            db.child('Tweets').push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = 'failed to tweet'
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    tweets = db.child('Tweets').get().val()
    return render_template("tweets.html", tweets = tweets)

if __name__ == '__main__':
    app.run(debug=True)