from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Length,Email,EqualTo,ValidationError
from main_pack import babel,gettext,lazy_gettext
from main_pack.models.users.models import Users,Rp_acc


class LogoImageForm(FlaskForm):
	logoImage = FileField('Company logo',validators=[FileAllowed(['jpg','png','img','gif','svg'])])


class SliderImageForm(FlaskForm):
	sliderImageTitle = StringField()
	sliderImageDesc = StringField()
	sliderImage = FileField('Slider Image',validators=[
		FileAllowed(['jpg','png','img','gif'])])
	SlImgStartDate = StringField('Start date')
	SlImgEndDate = StringField('End date')


class UserRegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField('Email',
						validators=[DataRequired(),Email(),Length(max=225)])
	full_name = StringField(lazy_gettext('Full name'))
	user_type = SelectField('User type',coerce=int)
	picture = FileField(lazy_gettext('Avatar'),
							validators=[FileAllowed(['jpg','png','img','svg','gif','bmp'])])
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	confirm_password = PasswordField (lazy_gettext('Confirm password'),
									validators=[DataRequired(),EqualTo('password')])

	def validate_username(self,username):
		user = Users.query.filter_by(UName=username.data).first()
		if user:
			raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))
	def validate_email(self,email):
		user = Users.query.filter_by(UEmail=email.data).first()
		if user:
			raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))


class CustomerRegistrationForm(FlaskForm):
	username = StringField('Username', 
							validators=[DataRequired(),Length(min=2,max=60)])
	email = StringField('Email',
						validators=[DataRequired(),Email(),Length(max=225)])
	full_name = StringField(lazy_gettext('Full name'))	
	customer_type = SelectField('Customer type',coerce=int)
	vendor_user = SelectField('Vendor user',coerce=int)
	address = StringField(lazy_gettext('Address'),
							validators=[Length(max=255)])
	mobilePhone = StringField(lazy_gettext('Mobile phone'))
	homePhone = StringField(lazy_gettext('Home phone'))
	zipCode = StringField(lazy_gettext('Zip code'),
							validators=[Length(max=225)])
	picture = FileField(lazy_gettext('Avatar'),
							validators=[FileAllowed(['jpg','png','img','svg','gif','bmp'])])
	password = PasswordField(lazy_gettext('Password'),validators=[DataRequired()])
	confirm_password = PasswordField (lazy_gettext('Confirm password'),
									validators=[DataRequired(),EqualTo('password')])

	def validate_username(self,username):
		rp_acc = Rp_acc.query.filter_by(RpAccUName=username.data).first()
		user = Users.query.filter_by(UName=username.data).first()
		if rp_acc or user:
			raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))
		
	def validate_email(self,email):
		rp_acc = Rp_acc.query.filter_by(RpAccEMail=email.data).first()
		user = Users.query.filter_by(UEmail=email.data).first()
		if rp_acc or user:
			raise ValidationError(lazy_gettext('That email is taken. Choose a different one!'))