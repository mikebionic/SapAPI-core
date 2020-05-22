from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,ValidationError


class LogoImageForm(FlaskForm):
		logoImage = FileField('Company logo', validators=[FileAllowed(['jpg','png','img'])])
		submit = SubmitField('Upload')


class SliderImageForm(FlaskForm):
		sliderImage = FileField('Slider Image', validators=[FileAllowed(['jpg','png','img'])])
		submit = SubmitField('Upload')

class UploadFileForm(FlaskForm):
		file = FileField('Upload File')
		submit = SubmitField('Upload')