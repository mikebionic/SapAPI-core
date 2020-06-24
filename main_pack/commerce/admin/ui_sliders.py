from flask import render_template,url_for,json,jsonify,session,flash,redirect,request,Response, abort
from main_pack import db,babel,gettext
from flask_login import current_user,login_required
from datetime import datetime
from main_pack.commerce.admin import bp

from main_pack.models.base.models import Slider,Sl_image
from main_pack.commerce.admin.utils import addSliderDict,addSliderImageDict

@bp.route('/ui/slider/', methods=['GET','POST','PUT'])
def ui_sliders():
	if request.method == 'POST':
		req = request.get_json()
		slider = addSliderDict(req)
		print(slider)
		sliderId = req.get('sliderId')
		print(sliderId)
		# try:
		if (sliderId == '' or sliderId == None):
			print('committing')
			newSlider = Slider(**slider)
			db.session.add(newSlider)
			db.session.commit()
			response = jsonify({
				'sliderId':newSlider.SlId,
				'status':'created',
				'responseText':gettext('Slider')+' '+gettext('successfully saved'),
				'htmlData': render_template('commerce/admin/sliderAppend.html',slider=newSlider)
				})
		else:
			print('updating')
			thisSlider = Slider.query.get(sliderId)
			print(thisSlider.SlId)
			thisSlider.update(**slider)
			db.session.commit()
			response = jsonify({
				'status':'updated',
				'responseText':gettext('Slider')+' '+gettext('successfully updated'),
				})
		# except:
		# 	response = jsonify({
		# 		'status':'error',
		# 		'responseText':gettext('Unknown error!'),
		# 		})
	return response

@bp.route('/ui/sl_image/', methods=['GET','POST','PUT'])
def ui_sl_image():
	if request.method == 'POST':
		req = request.get_json()
		sl_image = addSliderImageDict(req)
		print(sl_image)

		sliderImgId = req.get('sliderImgId')
		print(sliderImgId)
		if (sliderImgId == '' or sliderImgId == None):
			try:
				print('committing')
				newSliderImage = Sl_image(**sl_image)
				db.session.add(newSliderImage)
				db.session.commit()
				response = jsonify({
					'sliderImgId':newSliderImage.sliderImgId,
					'status':'created',
					'responseText':gettext('Slider image')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/sliderImageAppend.html',sl_image=newSliderImage)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response
