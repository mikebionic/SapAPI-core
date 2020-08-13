from flask_wtf import FlaskForm
from wtforms import (StringField,
										PasswordField,
										SubmitField,
										BooleanField)
from wtforms.validators import (DataRequired,
																Length,
																Email,
																EqualTo,
																ValidationError)
from main_pack import babel,gettext,lazy_gettext
from main_pack.models_test.users.models import Users


class RequestRegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField ('Email',
						validators=[DataRequired(),Email(),Length(max=100)])
	submit = SubmitField('Proceed')

	def validate_username(self,username):
		user = Users.query.filter_by(UName=username.data).first()
		if user:
			raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))
	def validate_email(self,email):
		user = Users.query.filter_by(UEmail=email.data).first()
		if user:
			raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))


class PasswordRegistrationForm(FlaskForm):
	full_name = StringField(lazy_gettext('Full name'), 
							validators=[DataRequired(),Length(min=2,max=100)])
	phone_number = StringField(lazy_gettext('Phone number'), 
							validators=[DataRequired(),Length(min=2,max=100)])
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	confirm_password = PasswordField (lazy_gettext('Confirm password'),
									validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField(lazy_gettext('Sign Up'))


class AdminLoginForm(FlaskForm):
	username = StringField (lazy_gettext('Username'),
						validators=[DataRequired()])
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	remember = BooleanField(lazy_gettext('Remember Me'))
	submit = SubmitField(lazy_gettext('Log In'))


class LoginForm(FlaskForm):
	email = StringField (lazy_gettext('Email'),
						validators=[DataRequired(),Email()])
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	remember = BooleanField(lazy_gettext('Remember Me'))
	submit = SubmitField(lazy_gettext('Log In'))


class RequestResetForm(FlaskForm):
	email = StringField (lazy_gettext('Email'),
						validators=[DataRequired(),Email()])
	submit = SubmitField(lazy_gettext('Request Password Reset'))

	def validate_email(self,email):
		user = Users.query.filter_by(UEmail=email.data).first()
		if user is None:
			raise ValidationError(lazy_gettext('The profile of that email not found! Please register fist.'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	confirm_password = PasswordField(lazy_gettext('Confirm password'),
									validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField(lazy_gettext('Reset password'))