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