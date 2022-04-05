# -*- coding: utf-8 -*-
from flask import request, abort

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.rating_api import api
from main_pack.api.v1.rating_api.utils import manage_rating
from main_pack.api.response_handlers import handle_default_response, handle_instertion_response

@bp.route('/v-ratings/',methods=['POST','DELETE'])
@token_required
def v_ratings(user):
	model_type = user['model_type']
	current_user = user['current_user']
	if (model_type == "user"):
		abort(400)

	req = request.get_json()
	data = manage_rating(req, model_type, current_user, request.method)
	return handle_default_response(data, "rating profile update")