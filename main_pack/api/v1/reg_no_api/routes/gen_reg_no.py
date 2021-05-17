# -*- coding: utf-8 -*-
from flask import render_template,url_for,jsonify,request,abort,make_response
from main_pack.api.base import api
from main_pack.config import Config

from main_pack import db,babel,gettext,lazy_gettext


from main_pack.models import User
from main_pack.api.auth.utils import token_required


@api.route("/gen-reg-no/",methods=['POST'])
@token_required
def gen_reg_no(user):
	model_type = user['model_type']
	current_user = user['current_user']
	req = request.get_json()
	data = generate_pred_reg_no(req)


	res = {
		"status": status,
		"data": data,
		"message": message
	}

	status_code = 200
	response = make_response(jsonify(res),status_code)
	return response