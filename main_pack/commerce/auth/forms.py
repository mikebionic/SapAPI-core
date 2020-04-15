from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main_pack.models.users.models import Users

class RequestRegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField ('Email',
						validators=[DataRequired(),Email(),Length(max=100)])
	submit = SubmitField('Proceed')

	def validate_username(self,username):
		user = Users.query.filter_by(UName=username.data).first()
		if user:
			raise ValidationError('That username is taken. Choose a different one!')
	def validate_email(self,email):
		user = Users.query.filter_by(UEmail=email.data).first()
		if user:
			raise ValidationError('That email is taken. Choose a different one!')

class PasswordRegistrationForm(FlaskForm):
	full_name = StringField('Full name', 
							validators=[DataRequired(),Length(min=2,max=100)])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField ('Confirm Password',
									validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField ('Email',
						validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log In')


class RequestResetForm(FlaskForm):
	email = StringField ('Email',
						validators=[DataRequired(),Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self,email):
		user = Users.query.filter_by(UEmail=email.data).first()
		if user is None:
			raise ValidationError('The account of that email not found! Please register fist.')

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm password',
									validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Reset password')