# -*- coding: utf-8 -*-
from datetime import datetime

from main_pack import Config
from main_pack.base.apiMethods import checkApiResponseStatus
from main_pack.base import get_first_from_list

from .collect_order_inv_models import collect_order_inv_models
from .generate_order_inv_json import generate_order_inv_json

def collect_order_inv_data(
	single_object = False,
	invoices_only = False,
	show_inv_line_resource = False,
	rp_acc_user = None,
	currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE,
	**kwargs,
	# startDate = None,
	# endDate = datetime.now(),
	# statusId = None,
	# invoice_list = None,
	# invoice_models = None,
	# DivId = None,
	# notDivId = None,
):

	invoice_models = collect_order_inv_models(
		rp_acc_user = rp_acc_user,
		**kwargs
	)

	data, fails = generate_order_inv_json(
		invoice_models = invoice_models,
		rp_acc_user = rp_acc_user,
		invoices_only = invoices_only,
		currency_code = currency_code,
		show_inv_line_resource = show_inv_line_resource
	)

	status = checkApiResponseStatus(data, fails)
	if single_object:
		data = get_first_from_list(data)
		fails = get_first_from_list(fails)

	res = {
			"message": "Order invoice",
			"data": data,
			"fails": fails,
			"total": len(data) if not single_object else 1 if data else 0,
			"fail_total": len(fails) if not single_object else 1 if fails else 0
	}
	for e in status:
		res[e] = status[e]
	return res