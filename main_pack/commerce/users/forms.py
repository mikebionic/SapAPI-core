from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from main_pack.models.users.models import Users
from main_pack import babel,gettext,lazy_gettext

class UpdateProfileForm(FlaskForm):
	username = StringField(lazy_gettext('Username'), 
							validators=[DataRequired(), Length(min=3, max=40)])
	fullname = StringField(lazy_gettext('Full name'),
							validators=[DataRequired()])
	picture = FileField(lazy_gettext('Update Profile Picture'), validators=[FileAllowed(['jpg','png','img'])])
	submit = SubmitField(lazy_gettext('Update'))

	def validate_username(self,username):
		if username.data != current_user.UName:
			user = Users.query.filter_by(UName=username.data).first()
			if user:
				raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))

	# RpAccName = db.Column(db.String(255))
	# RpAccAddress = db.Column(db.String(500))
	# RpAccMobilePhoneNumber = db.Column(db.String(100))
	# RpAccHomePhoneNumber = db.Column(db.String(100))
	# RpAccZipCode = db.Column(db.String(100))
	# RpAccEMail = db.Column(db.String(100))
	# RpAccFirstName = db.Column(db.String(100))
	# RpAccLastName = db.Column(db.String(100))
	# RpAccPatronomic = db.Column(db.String(100))
	# RpAccBirthDate = db.Column(db.DateTime)
	# RpAccResidency = db.Column(db.String(100))


class UpdateCommerceProfileForm(FlaskForm):
	rpAccName = StringField(lazy_gettext('Name'), 
							validators=[DataRequired(), Length(min=3, max=255)])
	rpAccName = StringField(lazy_gettext('Username'), 
							validators=[DataRequired(), Length(min=3, max=40)])
	rpAccName = StringField(lazy_gettext('Username'), 
							validators=[DataRequired(), Length(min=3, max=40)])
	rpAccName = StringField(lazy_gettext('Username'), 
							validators=[DataRequired(), Length(min=3, max=40)])
	rpAccName = StringField(lazy_gettext('Username'), 
							validators=[DataRequired(), Length(min=3, max=40)])
	picture = FileField(lazy_gettext('Update Profile Picture'), validators=[FileAllowed(['jpg','png','img'])])
	submit = SubmitField(lazy_gettext('Update'))

	def validate_username(self,username):
		if username.data != current_user.UName:
			user = Users.query.filter_by(UName=username.data).first()
			if user:
				raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))

