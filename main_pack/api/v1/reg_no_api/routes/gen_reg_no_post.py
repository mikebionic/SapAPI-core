# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response

from main_pack.api.v1.reg_no_api import api
from main_pack.api.v1.reg_no_api.utils import generate_pred_reg_no
from main_pack.api.auth.utils import token_required


@api.route("/gen-reg-no/", methods=['POST'])
@token_required
def gen_reg_no_post(user):
	model_type = user['model_type']
	current_user = user['current_user']

	req = request.get_json()
	data = generate_pred_reg_no(req, model_type, current_user)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Pred Reg_no generation"
	}

	return make_response(jsonify(res), 200)