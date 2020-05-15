from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp
from main_pack.commerce.commerce.utils import commonUsedData,realResRelatedData
from main_pack.models.commerce.models import Resource,Res_category


@bp.route("/product/ui_cart/", methods=['POST','PUT'])
def ui_cart():
	commonData = commonUsedData()
	resData = realResRelatedData()
	if request.method == "POST":
		try:
			req = request.get_json()
			resId = req.get('resId')
			resource = Resource.query.get(resId)
			resourceQty='single'
			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					resource=resource,**commonData,**resData,resourceQty=resourceQty)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
		resources=[]
		req = request.get_json()
		try:
			for resElement in req:
				resId = req[resElement].get('resId')
				resource = Resource.query.get(resId)
				resources.append(resource)
			resourceQty='multi'
			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					resources=resources,**commonData,**resData,resourceQty=resourceQty)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response