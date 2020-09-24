from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from main_pack import babel,gettext,lazy_gettext
from wtforms.widgets import TextArea

class SendEmailToCompanyForm(FlaskForm):
	FirstName = StringField(validators=[DataRequired()])
	LastName = StringField(validators=[DataRequired()])
	Email = StringField(validators=[DataRequired()])
	Phone = StringField()
	Message = StringField(validators=[DataRequired()],widget=TextArea())