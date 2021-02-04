from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
	StringField,
	PasswordField,
	SubmitField,
	BooleanField,
	SelectField)
from wtforms.widgets import TextArea
from wtforms.validators import (
	DataRequired,
	Length,
	Length,
	Email,
	EqualTo,
	ValidationError)
from main_pack import lazy_gettext

from main_pack.models.users.models import Users,Rp_acc


class LogoImageForm(FlaskForm):
	logoImage = FileField(validators=[FileAllowed(['jpg','png','img','gif','svg'])])


class SliderImageForm(FlaskForm):
	sliderImageTitle = StringField()
	sliderImageDesc = StringField()
	sliderImage = FileField(validators=[FileAllowed(['jpg','png','img','gif'])])
	SlImgStartDate = StringField()
	SlImgEndDate = StringField()


class ResourceEditForm(FlaskForm):
	resourceImage = FileField(validators=[FileAllowed(['jpg','png','img'])])
	ResName = StringField(validators=[DataRequired(),Length(min=2,max=255)])
	ResDesc = StringField(validators=[Length(max=500)])
	ResFullDesc = StringField(validators=[Length(max=1500)],widget=TextArea())
	BrandId = SelectField(coerce=int)


class BrandForm(FlaskForm):
	BrandName = StringField(validators=[DataRequired()])
	BrandDesc = StringField()
	BrandVisibleIndex = StringField()
	IsMain = BooleanField()
	BrandLink1 = StringField()
	BrandLink2 = StringField()
	BrandLink3 = StringField()
	BrandLink4 = StringField()
	BrandLink5 = StringField()
	Image = FileField(validators=[FileAllowed(['jpg','png','img','gif','svg'])])


class UserForm(FlaskForm):
	username = StringField(validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField(validators=[DataRequired(),Email(),Length(max=225)])
	full_name = StringField()
	user_type = SelectField(coerce=int)
	picture = FileField(validators=[FileAllowed(['jpg','png','img','svg','gif','bmp'])])
	password = PasswordField(validators=[DataRequired()])
	confirm_password = PasswordField(validators=[DataRequired(),EqualTo('password')])

	def validate_username(self,username):
		user = Users.query.filter_by(UName = username.data, GCRecord = None).first()
		if user:
			# flash(lazy_gettext('That username is taken. Choose a different one!'),'warning')
			raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))
	def validate_email(self,email):
		user = Users.query.filter_by(UEmail = email.data, GCRecord = None).first()
		if user:
			# flash(lazy_gettext('That email is taken. Choose a different one!'),'warning')
			raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))


class RpAccForm(FlaskForm):
	username = StringField(validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField(validators=[DataRequired(),Email(),Length(max=225)])
	full_name = StringField()	
	rp_acc_type = SelectField(coerce=int)
	user = SelectField(coerce=int)
	address = StringField(validators=[Length(max=255)])
	mobilePhone = StringField()
	homePhone = StringField()
	zipCode = StringField(validators=[Length(max=225)])
	picture = FileField(validators=[FileAllowed(['jpg','png','img','svg','gif','bmp'])])
	password = StringField(validators=[DataRequired()])
	confirm_password = StringField(validators=[DataRequired(),EqualTo('password')])

	# def validate_username(self,username):
	# 	rp_acc = Rp_acc.query.filter_by(RpAccUName=username.data).first()
	# 	if rp_acc:
	# 		raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))
		
	# def validate_email(self,email):
	# 	rp_acc = Rp_acc.query.filter_by(RpAccEMail=email.data).first()
	# 	if rp_acc:
	# 		raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))