from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField,FormField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError
from main_pack import babel,gettext,lazy_gettext

class LogoImageForm(FlaskForm):
	logoImage = FileField('Company logo',validators=[FileAllowed(['jpg','png','img','svg','gif'])])

class SliderImageForm(FlaskForm):
	sliderImageDesc = StringField()
	sliderImage = FileField('Slider Image',validators=[FileAllowed(['jpg','png','img','svg','gif'])])