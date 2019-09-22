from flask import Flask,render_template,redirect,request,url_for,session
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from . import auth
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User,bcrypt

@auth.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
      user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
      db.session.add(user)
      db.session.commit()
      login_user(user)
      return redirect(url_for('auth.login'))
    return render_template("register.html",form=form)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
      if form.validate_on_submit():
        user = User.query.filter_by(name=request.form['username']).first()
        if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
          login_user(user)
          return redirect(url_for('frontend.dashboard'))
       # if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        else:
          error = 'Invalid Credentials. Please try again.'
    return render_template("login.html",error=error,form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
