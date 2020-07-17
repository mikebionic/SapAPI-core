from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired,Length,ValidationError
from main_pack import babel,gettext,lazy_gettext

class LogoImageForm(FlaskForm):
	logoImage = FileField('Company logo',validators=[FileAllowed(['jpg','png','img','gif','svg'])])

class SliderImageForm(FlaskForm):
	sliderImageDesc = StringField()
	sliderImage = FileField('Slider Image',validators=[
		FileAllowed(['jpg','png','img','gif'])])
	SlImgStartDate = StringField('Start date')
	SlImgEndDate = StringField('End date')