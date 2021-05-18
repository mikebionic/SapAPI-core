# -*- coding: utf-8 -*-
from flask import (
	request,
	session,
	jsonify,
	make_response,
)
from flask_login import login_required, current_user

from main_pack.commerce.commerce import bp
from main_pack.api.v1.reg_no_api.utils import generate_pred_reg_no


@bp.route("/commerce/ui-gen-reg-no/", methods=['POST'])
@login_required
def ui_gen_reg_no():
	req = request.get_json()
	data = generate_pred_reg_no(req, session["model_type"], current_user)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Pred Reg_no generation"
	}

	return make_response(jsonify(res), 200)