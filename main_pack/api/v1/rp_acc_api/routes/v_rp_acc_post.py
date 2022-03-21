# -*- coding: utf-8 -*-
from flask import request, abort

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.rp_acc_api import api
from main_pack.api.v1.rp_acc_api.utils import save_rp_acc_req_data, update_rp_acc_profile
from main_pack.api.response_handlers import handle_default_response, handle_instertion_response


@api.route("/v-rp-accs/", methods=['POST'])
@token_required
@request_is_json(request)
def v_rp_acc_post(user):
	model_type = user['model_type']
	current_user = user['current_user']
	if (model_type == "rp_acc"):
		abort(400)

	req = request.get_json()
	data, fails = save_rp_acc_req_data(req, model_type, current_user)

	return handle_instertion_response(data, fails, "Rp_acc_management")


@api.route("/v-rp-accs/profile-edit/", methods=['POST'])
@token_required
@request_is_json(request)
def v_rp_accs_profile_edit(user):
	model_type = user['model_type']
	current_user = user['current_user']
	if (model_type == "user"):
		abort(400)

	req = request.get_json()
	data, fails = update_rp_acc_profile(req, model_type, current_user)
	return handle_instertion_response(data, fails, "Rp_acc profile update")