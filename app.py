from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import os 

#instantiating app object
app = Flask(__name__)

#secret key 
app.secret_key= os.environ.get('SECRET_KEY', 'my_dev_secret_key')

#setting up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#creating a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'{self.username}'


#basic route with an end point of /home
#home route 
@app.route('/', methods=['GET','POST'])
def hello():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password','')
        errors = []
        if not username:
            errors.append("username required")
        if not email:
            errors.append(" email requires")
        if not password:
            errors.append(" password required")

        if errors:
            return render_template('index.html', username=username, errors=errors, email=email, password=password)
        hashed = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed)
        
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('User with that username or email already exists', 'danger')
            return render_template('index.html')
        flash('User regisered successfully ')

        #set session 
        session['username'] = user.email
        session['email'] = user.email

        return redirect(url_for('dashboard'))
    return render_template('index.html')
#Implementing a dynamic route using the variable name (username)
#converter is a string
 
#login route 
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password','')

        errors = []
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            errors.append('Invalid username or password')
            return render_template('index.html', errors=errors, username=username, email=email)

        session['username'] = user.username
        session['email'] = user.email
        flash('User logged in successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

#dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', username=session.get('username'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
