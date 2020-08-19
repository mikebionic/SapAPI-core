from flask import render_template,url_for,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext

# auth and validation
from flask_login import current_user,login_required
from main_pack.commerce.auth.utils import ui_admin_required
# / auth and validation /

from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.models.base.models import Slider,Sl_image
from main_pack.commerce.admin.utils import addSliderDict,addSliderImageDict

@bp.route('/ui/slider/', methods=['POST','DELETE'])
@login_required
@ui_admin_required()
def ui_sliders():
	try:
		if request.method == 'POST':
			req = request.get_json()
			slider = addSliderDict(req)
			sliderId = req.get('sliderId')
			SlName = slider['SlName']
			# check for slider presense in database
			slider_model = Slider.query\
				.filter_by(GCRecord = None, SlName = SlName)\
				.first()
			if slider_model:
				response = jsonify({
					"status": "error",
					"responseText": gettext('Slider')+' '+gettext('already present'),
					"htmlData":  render_template('commerce/admin/sliderAppend.html',slider=newSlider)
				})
				return response
			if (sliderId == '' or sliderId == None):
				print('committing')
				newSlider = Slider(**slider)
				db.session.add(newSlider)
				db.session.commit()
				response = jsonify({
					"sliderId": newSlider.SlId,
					"status": "created",
					"responseText": gettext('Slider')+' '+gettext('successfully saved'),
					"htmlData":  render_template('commerce/admin/sliderAppend.html',slider=newSlider)
				})
			else:
				print('updating')
				thisSlider = Slider.query.get(sliderId)
				thisSlider.update(**slider)
				db.session.commit()
				response = jsonify({
					"status": "updated",
					"responseText": gettext('Slider')+' '+gettext('successfully updated'),
				})			
		elif request.method == 'DELETE': 
			req = request.get_json()
			sliderId = req.get('sliderId')
			thisSlider = Slider.query.get(sliderId)
			thisSlider.GCRecord = 1
			db.session.commit()
			response = jsonify({
				"status": "deleted",
				"responseText": gettext('Slider')+' '+gettext('successfully deleted'),
			})
	except Exception as ex:
		print(ex)
		response = jsonify({
			"status": "error",
			"responseText": gettext('Unknown error!'),
		})
	return response
