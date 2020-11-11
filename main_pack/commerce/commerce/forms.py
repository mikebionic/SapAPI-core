from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import (
	DataRequired,
	Length,
	Email,
	EqualTo,
	ValidationError)

class SendEmailToCompanyForm(FlaskForm):
	FirstName = StringField(validators=[DataRequired()])
	LastName = StringField(validators=[DataRequired()])
	Email = StringField(validators=[DataRequired(),Email()])
	Phone = StringField()
	Message = StringField(validators=[DataRequired()],widget=TextArea())