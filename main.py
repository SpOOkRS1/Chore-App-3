###################################################
# Starting and linking Flask together with SQL
###################################################
#importing what we need 
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

# creating an instance of a flask application.
app = Flask(__name__)

#find the directory we are currently in
dir_path = os.path.dirname(os.path.realpath(__file__))

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#starts our data base
db = SQLAlchemy(app)
###################################################



##################################################
# Creating a User Table
##################################################
class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    names = db.Column(db.Text)
    name_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.Text)
  names = db.relationship('Name')

  def __init__(self,description):
    self.description = description
  
  def __repr__(self):
    return (f"Description:{self.description}")

db.create_all()
#####################################################
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

@app.route('/')
def home():

  return render_template('home.html')

@app.route('/login')
def login():

  return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')

        if len(name) <= 1:
            flash('Name is too short!', category='error')
        else:
            new_name = Name(data=name, name_id=current_user.id)
            db.session.add(new_name)
            db.session.commit()
            flash('Name added!', category='success')

    return render_template("admin.html")


@app.route('/adlogin', methods=['GET', 'POST'])
def adlogin():
    if request.method == 'POST':
      flash('Logged in successfully!', category='success')
      return redirect(url_for('admin'))
    return render_template('adlogin.html', user=current_user)

# Creating a route for the add page
@app.route('/add')
def add():
  # render the add page
  return render_template('add.html')

# Creating a route for when we submit the add form 
# Notice we will render index.html here
@app.route('/added')
def added():
  # Get the username and name from the form we submited
  username = request.args.get('username')
  name = request.args.get('name')

  # Create a new user based on the arguments 
  newUser = User(username,name)
  # Add it to the database
  db.session.add(newUser)
  db.session.commit()

  # Create a message 
  message = f"We have added a new user: {username} "
  # Load a list of all the users from the UserDatabase
  userList = User.query.all()
  # Render the template passing in the user list and the message
  return render_template('index.html',userList=userList,message=message)

if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.run(debug=True,host='0.0.0.0')


# As of April 5, 2021 this is the last line of code that has been written. Every thing as of right now works.