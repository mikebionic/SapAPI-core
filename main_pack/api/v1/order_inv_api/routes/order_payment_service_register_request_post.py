from flask import (
	make_response,
	jsonify,
	request,
	session,
	url_for,
)

from main_pack.api.auth.utils import token_required
from main_pack.api.base.validators import request_is_json

from main_pack.api.v1.order_inv_api import api
from main_pack.api.common import (
	get_UserId_and_RpAccId_from_login_and_uuid_info,
	get_CurrencyCode_from_req_or_session,
	get_currency_model_from_code,
)
from main_pack.api.v1.order_inv_api.utils import do_halkbank_payment_service_register_request, do_InterActiv_payment_service_register_request

@api.route("/order-payment-register-request/", methods=['POST'])
@token_required
@request_is_json(request)
def order_payment_service_register_request_post(user):
	current_user = user['current_user']
	online_payment_type = request.args.get("online_payment_type", "halkbank", type=str).strip()
	paym_validation_view = url_for('commerce.render_payment_validation_view')[1:] if url_for('commerce.render_payment_validation_view')[0] == "/" else url_for('commerce.render_payment_validation_view')
	return_url = f"{request.url_root}{paym_validation_view}"
	data = {}
	try:
		req = request.get_json()
		currency_code = get_CurrencyCode_from_req_or_session(req, session)
		req["online_payment_type"] = online_payment_type
		
		if online_payment_type == "halkbank" and currency_code == "TMT":
			data = do_halkbank_payment_service_register_request(req, return_url)

		if online_payment_type == "foreign_affairs_bank":
			this_currency = get_currency_model_from_code(currency_code)
			if not this_currency:
				print("no currency column found during search")
				raise Exception

			_, _, _, rp_acc, _ = get_UserId_and_RpAccId_from_login_and_uuid_info(session["model_type"], current_user)

			data = do_InterActiv_payment_service_register_request(
				req,
				return_url,
				CurrencyNumCode = this_currency.CurrencyNumCode,
				CustomerName = rp_acc.RpAccName if rp_acc else None,
				CustomerEmail = rp_acc.RpAccEMail if rp_acc else None,
				CustomerHomePhone = rp_acc.RpAccHomePhoneNumber if rp_acc else None,
				CustomerMobilePhone = rp_acc.RpAccMobilePhoneNumber if rp_acc else None,
				UserAgent = request.user_agent,
				RemoteAddress = request.remote_addr,
				ScreenHeight = None,
				ScreenWidth = None,
			)

	except Exception as ex:
		print(ex)

	res = {
		"status": 1 if data else 0,
		"data": data,
		"message": "Payment register request",
	}

	status_code = 200 if data else 400

	return make_response(jsonify(res)), status_code
