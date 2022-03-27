# -*- coding: utf-8 -*-
from flask import request
import uuid

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json
from main_pack import Config, db
from main_pack.api.commerce.commerce_utils import apiResourceInfo

from main_pack.api.v1.rp_acc_api import api
from main_pack.api.response_handlers import handle_default_response, handle_instertion_response
from main_pack.models import Wish, Resource
from main_pack.base import log_print


@api.route('/v-wishlist/')
@token_required
def v_wishlist_get(user):
	model_type = user['model_type']
	current_user = user['current_user']
	page = request.args.get("page",1,type=int)

	filtering = {"GCRecord": None}
	if (model_type == "user"):
		filtering["UId"] = current_user.UId
	if (model_type == "rp_acc"):
		filtering["RpAccId"] = current_user.RpAccId

	pagination_wishes = Wish.query\
		.with_entities(Wish.ResId)\
		.filter_by(**filtering)\
		.order_by(Wish.CreatedDate.desc())\
		.paginate(per_page = Config.RESOURCES_PER_PAGE, page = page)

	product_list = [{'ResId': wish.ResId} for wish in pagination_wishes.items]
	return handle_default_response(apiResourceInfo(product_list)["data"])


@api.route('/v-wishlist/', methods=['POST','DELETE'])
@token_required
@request_is_json(request)
def v_wishlist_post(user):
	model_type = user['model_type']
	current_user = user['current_user']

	filtering = {"GCRecord": None}
	if (model_type == "user"):
		filtering["UId"] = current_user.UId
	if (model_type == "rp_acc"):
		filtering["RpAccId"] = current_user.RpAccId

	try:
		req = request.get_json()
		ResId = req.get("ResId")
		if not ResId:
			raise Exception
		
		filtering["ResId"] = ResId

		wish = Wish.query\
			.filter_by(**filtering)\
			.first()
		if request.method =="POST":
			if wish:
				log_print(f"Wishlist api | Wish already present by ResId={ResId}")
				raise Exception

			resource = Resource.query.with_entities(Resource.ResId)\
				.filter_by(GCRecord = None, ResId = ResId)\
				.first()
			if resource is None:
				log_print(f"Wishlist api | Resource none by id={ResId}")
				raise Exception

			filtering["WishGuid"] = uuid.uuid4()
			wish = Wish(**filtering)
			db.session.add(wish)
			db.session.commit()

			return handle_default_response(
				wish.to_json_api(),
				message = "Wish created!",
				status_code=201
			)
		
		if request.method=="DELETE":
			if not wish:
				raise Exception

			# wish.GCRecord = 1
			db.session.delete(wish)
			db.session.commit()
			return handle_default_response(filtering, message="Wish removed!", status_code=201)

	except Exception as ex:
		log_print(f"Wishlist api exception: {ex}")
		return handle_default_response(filtering, message=f"Wishlist error {ex}", status_code=400)
