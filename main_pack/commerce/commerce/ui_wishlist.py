
# from main_pack.api.commerce.commerce_utils import apiResourceInfo


# logi_required
# Rp_acc
# Wish
@bp.route('/product/ui_wishlist/',methods=['POST','DELETE'])
@login_required
def ui_wishlist():
	req = request.get_json()
	ResId = req.get("resId")
	RpAccId = current_user.RpAccId
	try:
		if request.method =="POST":
			# # check for presense of rp_acc (optional step)
			# rp_acc = Rp_acc.query\
			# 	.filter(and_(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None),\
			# 		Rp_acc.RpAccId==RpAccId).first()
			# if rp_acc is None:
			# 	raise Exception

			# check for presense of wish
			wish = Wish.query\
				.filter(and_(Wish.GCRecord=='' or Wish.GCRecord==None),\
					Wish.ResId==ResId,\
					Wish.RpAccId==RpAccId)\
				.first()
			# avoid double insertion
			if wish:
				raise Exception

			resource = Resource.query\
				.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),\
					Resource.ResId==ResId)\
				.first()
			# avoid insertion of Deleted or null resource
			if resource is None:
				raise Exception
			
			wish = {
				'RpAccId':RpAccId,
				'ResId':ResId,
			}
			wish = Wish(**wish)
			db.session.add(wish)
			db.session.commit()

			# product={}
			# product['ResId'] = ResId
			# product_list=[product]
			# resData = UiCartResourceData(product_list)

			response = jsonify({
				'status':'added',
				'responseText':gettext('Product')+' '+gettext('successfully saved!')
			})
		
		if request.method=="DELETE":,

	except:
		response = jsonify({
			'status':'error',
			'responseText':gettext('Unknown error!'),
			})

	return response
