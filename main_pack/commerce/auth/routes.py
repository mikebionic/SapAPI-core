from flask import render_template, url_for, jsonify, session, flash, redirect , request, Response, abort
from main_pack.commerce.auth import bp
from main_pack.commerce.auth.forms import (LoginForm,RequestResetForm,ResetPasswordForm,
								RequestRegistrationForm,PasswordRegistrationForm)
from main_pack.commerce.users.models import Users
from flask_login import login_user, current_user, logout_user
from main_pack import db, bcrypt
from main_pack.commerce.auth.utils import (send_reset_email,get_register_token,
								verify_register_token,send_register_email)

@bp.route("/login", methods=['GET', 'POST'])
def login_commerce():
	if current_user.is_authenticated:
		return redirect('/commerce')
	form = LoginForm()
	if form.validate_on_submit(): 
		user = Users.query.filter_by(EMail=form.email.data).first()
		if user and bcrypt.check_password_hash(user.UPass,form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect("/commerce")
		else:
			flash(f'Login Failed! Wrong email or password', 'danger')	
	return render_template('commerce/main/auth/login.html',title='Login', form=form)

@bp.route("/logout")
def logout_commerce():
	logout_user()
	return redirect('/commerce')

@bp.route("/resetPassword", methods=['GET','POST'])
def reset_request_commerce():
	if current_user.is_authenticated:
		return redirect('/commerce')
	form = RequestResetForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(EMail=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password','info')
		return redirect('/commerce/login')
	return render_template('commerce/main/auth/reset_request.html',title='Reset Password', form=form)

@bp.route("/resetPassword/<token>", methods=['GET','POST'])
def reset_token_commerce(token):
	if current_user.is_authenticated:
		return redirect('/commerce')
	user = Users.verify_reset_token(token)
	if user is None:
		flash('Token is invalid or expired','warning')
		return redirect('/commerce/resetPassword')
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
		user.UPass = hashed_password
		db.session.commit()
		flash('Your password has been updated!', 'success')
		return redirect ('/commerce/login')
	return render_template('commerce/main/auth/reset_token.html',title='Reset Password',form=form)

@bp.route("/register", methods=['GET', 'POST'])
def register_commerce():
	if current_user.is_authenticated:
		return redirect('/commerce')
	form = RequestRegistrationForm()
	if form.validate_on_submit():
		send_register_email(UName=form.username.data,EMail=form.email.data)
		flash('An email has been sent with instructions to register your account','info')
		return redirect('/commerce/register')
	return render_template('commerce/main/auth/register_request.html',title='Register',form=form)


@bp.route("/register/<token>", methods=['GET','POST'])
def register_token_commerce(token):
	if current_user.is_authenticated:
		return redirect('/commerce')
	new_user = verify_register_token(token)
	if not 'EMail' in new_user:
		flash('Token is invalid or expired','warning')
		return redirect('/commerce/register')
	form = PasswordRegistrationForm()
	if form.validate_on_submit():
		try:
			UName = new_user['UName']
			EMail = new_user['EMail']
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode() 
			user = Users(UName=UName, EMail=EMail, UPass=hashed_password)
			db.session.add(user)
			db.session.commit()
			flash('{}, your account has been created!'.format(UName), 'success')
			return redirect ('/commerce/login')
		except:
			flash('Error occured, please try again.', 'danger')
			return redirect('/commerce/register')
	return render_template('commerce/main/auth/register_token.html',title='Register', form=form)