from flask import flash

from flask_wtf import FlaskForm
from wtforms import (
	StringField,
	PasswordField,
	SubmitField,
	BooleanField
)
from wtforms.validators import (
	DataRequired,
	Length,
	Email,
	EqualTo,
	ValidationError
)
from main_pack import lazy_gettext
from main_pack.models import Rp_acc


class RequestRegistrationForm(FlaskForm):
	username = StringField(validators=[DataRequired(), Length(min=2, max=60)])
	email = StringField(validators=[DataRequired(), Email(), Length(max=100)])
	submit = SubmitField()

	def validate_username(self, username):
		user = Rp_acc.query.filter_by(RpAccUName = username.data, GCRecord = None).first()
		if user:
			flash(lazy_gettext('That username is taken. Choose a different one!'), 'warning')
			raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))

	def validate_email(self, email):
		user = Rp_acc.query.filter_by(RpAccEMail = email.data, GCRecord = None).first()
		if user:
			flash(lazy_gettext('That email is taken. Choose a different one!'), 'warning')
			raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))


class PasswordRegistrationForm(FlaskForm):
	full_name = StringField(validators=[DataRequired(),Length(min=2,max=100)])
	phone_number = StringField()
	address = StringField()
	password = PasswordField(validators=[DataRequired()])
	confirm_password = PasswordField(validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField()


class AdminLoginForm(FlaskForm):
	username = StringField(validators=[DataRequired()])
	password = PasswordField(validators=[DataRequired()])
	remember = BooleanField()
	submit = SubmitField()


class LoginForm(FlaskForm):
	email = StringField(validators=[DataRequired(),Email()])
	password = PasswordField(validators=[DataRequired()])
	remember = BooleanField()
	submit = SubmitField()


class RequestResetForm(FlaskForm):
	email = StringField(validators=[DataRequired(),Email()])
	submit = SubmitField()

	def validate_email(self,email):
		user = Rp_acc.query.filter_by(RpAccEMail = email.data).first()
		if user is None:
			flash(lazy_gettext('The profile of that email not found! Please register fist.'), 'warning')
			raise ValidationError(lazy_gettext('The profile of that email not found! Please register fist.'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(validators=[DataRequired()])
	confirm_password = PasswordField(validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField()