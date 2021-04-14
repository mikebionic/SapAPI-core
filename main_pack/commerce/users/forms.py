from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from main_pack.models import Rp_acc
from main_pack import gettext, lazy_gettext


class UpdateRpAccForm(FlaskForm):
	username = StringField(validators=[DataRequired(),Length(min=2,max=60)])
	fullname = StringField(validators=[DataRequired(),Length(min=2,max=100)])
	address = StringField(validators=[Length(max=500)])
	mobilePhone = StringField(validators=[DataRequired(),Length(min=2,max=100)])
	homePhone = StringField(validators=[Length(max=100)])
	workPhone = StringField(validators=[Length(max=100)])
	workFax = StringField(validators=[Length(max=100)])
	zipCode = StringField(validators=[Length(max=100)])
	webAddress = StringField(validators=[Length(max=255)])
	picture = FileField(validators=[FileAllowed(['jpg','png','img'])])
	submit = SubmitField()

	def validate_username(self,username):
		if username.data != current_user.RpAccUName:
			user = Rp_acc.query.filter_by(RpAccUName = username.data).first()
			if user:
				raise ValidationError(lazy_gettext('That username is taken. Choose a different one!'))

