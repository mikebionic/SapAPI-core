
from main_pack.api.commerce.commerce_utils import apiResourceInfo

@bp.route('/product/ui_wishlist/',methods=['POST'])
def ui_wishlist():
	req = request.get_json()
	InvRegNo = req.get("invRegNo")
	try:
		if InvRegNo:
			invModel = Invoice.query\
				.filter(and_(Invoice.GCRecord=='' or Invoice.GCRecord==None),\
					Invoice.InvRegNo==InvRegNo).first()
		elif OInvRegNo:
			invModel = Order_inv.query\
				.filter(and_(Order_inv.GCRecord=='' or Order_inv.GCRecord==None),\
					Order_inv.OInvRegNo==OInvRegNo).first()

		invModel.InvStatId = InvStatId
		db.session.commit()
		response = jsonify({
			'status':'updated',
			'responseText':gettext('Invoice status')+' '+gettext('successfully updated'),
		})
	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})
	return response


  product_list=[]
	if request.method == "POST":
		try:
			req = request.get_json()
			ResId = req.get('resId')

			product={}
			product['ResId'] = ResId
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