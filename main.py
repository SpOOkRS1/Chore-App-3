###################################################
# Starting and linking Flask together with SQL
###################################################
#importing what we need 
import os
from flask import Flask, render_template, request
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

class User(db.Model): 

  id = db.Column(db.Integer,primary_key=True)
  code = db.Column(db.Text)
  description = db.Column(db.Text)

  def __init__(self,code,description):
    self.code = code
    self.description = description
  
  def __repr__(self):
    return (f"Code: {self.code} Description:{self.description}")

db.create_all()
#####################################################


@app.route('/')
def login():

  return render_template('login.html')

@app.route('/admin')
def admin():

  return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

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


# As of April 5, 2021 this is the last line of code that has been written. Every thing as of right now works.