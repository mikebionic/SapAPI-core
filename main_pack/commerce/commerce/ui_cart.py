from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user,login_required
from main_pack import db,babel,gettext,lazy_gettext
from main_pack.commerce.commerce import bp

from main_pack.commerce.commerce.cart_utils import UiCartResourceData

@bp.route("/product/ui_cart/", methods=['POST','PUT'])
def ui_cart():
	product_list=[]
	if request.method == "POST":
		try:
			req = request.get_json()
			resId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['resId'] = resId
			product['productQty'] = productQty
			product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})

	elif request.method == "PUT":
		req = request.get_json()
		try:
			for resElement in req:
				resId = req[resElement].get('resId')
				productQty = req[resElement].get('productQty')
				
				product={}
				product['resId'] = resId
				product['productQty'] = productQty
				product_list.append(product)

			resData = UiCartResourceData(product_list)

			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartItemAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response

@bp.route("/product/ui_cart_table/", methods=['POST','PUT'])
def ui_cart_table():
	product_list=[]
	if request.method == "POST":
		try:

			req = request.get_json()
			resId = req.get('resId')
			productQty = req.get('productQty')

			product={}
			product['resId'] = resId
			product['productQty'] = productQty
			product_list.append(product)

			resData = UiCartResourceData(product_list)
			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
					**resData)
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
				productQty = req[resElement].get('productQty')
				
				product={}
				product['resId'] = resId
				product['productQty'] = productQty
				product_list.append(product)

			resData = UiCartResourceData(product_list)

			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!'),
				'htmlData':render_template('commerce/main/commerce/cartTableAppend.html',
					**resData)
				})
		except:
			response = jsonify({
				'status':'error',
				'responseText':gettext('Unknown error!'),
				})
	return response