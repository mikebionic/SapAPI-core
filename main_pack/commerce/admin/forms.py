from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,SubmitField,BooleanField,TextAreaField,FormField,SelectField
from wtforms.validators import DataRequired,Length,ValidationError
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce.order_utils import invStatusesSelectData
from main_pack.commerce.admin import bp

# from main_pack.models.commerce.models import Inv_status

# def invStatusesSelectData():
# 	invStatusesList=[]
# 	inv_statuses = Inv_status.query\
# 	.filter(Inv_status.GCRecord=='' or Inv_status.GCRecord==None).all()
# 	for inv_status in inv_statuses:
# 		status = dataLangSelector(inv_status.to_json_api())
# 		obj=(status['InvStatId'],status['InvStatName'])
# 		invStatusesList.append(obj)
# 	return invStatusesList



class LogoImageForm(FlaskForm):
	logoImage = FileField('Company logo', validators=[FileAllowed(['jpg','png','img'])])


class SliderImageForm(FlaskForm):
	sliderImage = FileField('Slider Image', validators=[FileAllowed(['jpg','png','img'])])


class InvStatusForm(FlaskForm):
	invStatus = SelectField(lazy_gettext('Status'),validators=[DataRequired()])
	submit = SubmitField(lazy_gettext('Set'))