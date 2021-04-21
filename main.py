###################################################
# Starting and linking Flask together with SQL
###################################################
#importing what we need 
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
class Namez(db.Model): 
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.Text)

  def __init__(self,name):
    self.name = name
  
  def __repr__(self):
    return (f"NAME:{self.name}")

class Admin(db.Model, UserMixin): 
  id = db.Column(db.Integer,primary_key=True)
  adname = db.Column(db.String(150))

  def is_authenticated(self):
    return True

  def __init__(self,adname):
    self.adname = adname
  
  def __repr__(self):
    return (f"ADNAME: {self.adname}")

db.create_all()
#####################################################
login_manager = LoginManager()
login_manager.login_view = 'adlogin.html'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
  return Admin.query.get(int(id))

@app.route('/')
def home():

  return render_template('home.html')

@app.route('/login')
def login():

  return render_template('login.html')

@app.route('/adsign-up', methods=['GET', 'POST'])
def adsign_up():
    if request.method == 'POST':
        adname = request.form.get('adname')

        admin = Admin.query.filter_by(adname=adname).first()
        if admin:
            flash('Admin already exists', category='error')
        elif len(adname) < 2:
            flash('Firstname must be longer than 1 character.', category = 'error')
        #elif password1 != password2:
            #flash('Passwords do not match.', category = 'error')
        #elif len(password1) < 7:
            #flash('Password must be longer than 6 characters.', category = 'error')
        else:
            # add user to the data base
            new_admin = Admin(adname=adname)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            flash(f'Account created! Welcome {new_admin}', category = 'success')
            return redirect(url_for('admin'))

    return render_template('adsign_up.html', user=current_user)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
  userList = Namez.query.all()
  return render_template("admin.html", userList=userList)



@app.route('/adlogin', methods=['GET', 'POST'])
def adlogin():
    if request.method == 'POST':
      adname = request.form.get('adname')

      admin = Admin.query.filter_by(adname=adname).first()
      if admin:
        flash(f'Logged in successfully! Welcome {adname}!', category='success')
        login_user(admin, remember=True)
        return redirect(url_for('admin'))
      else:
        flash('Admin does not exist', category='error')

    return render_template('adlogin.html')



@app.route('/add')
def add():
  return render_template('add.html')



@app.route('/added')
def added():
  name = request.args.get('name')
  newPerson = Namez(name)
  db.session.add(newPerson)
  db.session.commit()
  userList = Namez.query.all()
  return render_template('admin.html',userList=userList)

######################################################################
if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.run(debug=True,host='0.0.0.0')


# As of April 5, 2021 this is the last line of code that has been written. Every thing as of right now works.