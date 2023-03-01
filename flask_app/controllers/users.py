from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/', methods=['GET', 'POST'])
def login_and_register():
    if request.method == 'POST':
        if not User.validate_registration(request.form):
            return redirect('/')
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user = User(**data)
        user.register()
        return render_template('profile.html', user=user)
    else:
        return render_template('login_and_registration.html')
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['login_email']
    user = User.get_by_email(email)
    if not user:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['login_password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user.id
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
