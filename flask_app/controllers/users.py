from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User

@app.route('/', methods=['GET', 'POST'])
def login_and_register():
    if request.method == 'POST':
        if not User.validate_registration(request.form):
            return redirect('/')
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        user = User(**data)
        user.register()
        return render_template('profile.html')
    else:
        return render_template('login_and_registration.html')
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['login_email']
    password = request.form['login_password']
    user = User.get_by_email(email)
    if user and user.password == password:
        session['user_id'] = user.id
        return render_template('profile.html', user=user)
    else:
        flash('Invalid email or password')
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
