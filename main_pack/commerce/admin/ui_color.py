from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.admin import bp
from main_pack.commerce.admin.utils import addCategoryDict
from main_pack.models.commerce.models import Color,Size,Size_type,Unit,Brand,Barcode

from main_pack.models.commerce.models import Size_type,Res_color,Res_sizens,Res_unit,Usage_status,Res_translations


@bp.route('/admin/resource/color/', methods=['GET','POST','PUT'])
def resource_color():
	if request.method == 'POST':
		req = request.get_json()
		color = addColorDict(req)
		colorId = req.get('colorId')
		if (colorId == '' or colorId == None):
			try:
				newColor = Color(**color)
				db.session.add(newColor)
				db.session.commit()
				response = jsonify({
					'colorId':newColor.colorId,
					'status':'created',
					'responseText':gettext('Color')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/colorAppend.html',color=newColor)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response

@bp.route('/admin/resource/size/', methods=['GET','POST','PUT'])
def resource_size():
	if request.method == 'POST':
		req = request.get_json()
		size = addSizeDict(req)
		sizeId = req.get('sizeId')
		if (sizeId == '' or sizeId == None):
			try:
				newSize = Size(**size)
				db.session.add(newSize)
				db.session.commit()
				response = jsonify({
					'sizeId':newSize.sizeId,
					'status':'created',
					'responseText':gettext('Size')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/sizeAppend.html',size=newSize)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response

@bp.route('/admin/resource/brand/', methods=['GET','POST','PUT'])
def resource_brand():
	if request.method == 'POST':
		req = request.get_json()
		brand = addBrandDict(req)
		brandId = req.get('brandId')
		if (brandId == '' or brandId == None):
			try:
				newBrand = Brand(**brand)
				db.session.add(newBrand)
				db.session.commit()
				response = jsonify({
					'brandId':newBrand.brandId,
					'status':'created',
					'responseText':gettext('Brand')+' '+gettext('successfully saved'),
					'htmlData': render_template('commerce/admin/brandAppend.html',brand=newBrand)
					})
			except:
				response = jsonify({
					'status':'error',
					'responseText':gettext('Unknown error!'),
					})
	return response