# -*- coding: utf-8 -*-
from datetime import datetime
import dateutil.parser
from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload

from main_pack.models.commerce.models import Order_inv,	Order_inv_line

def collect_order_invoice_models(
	startDate = None,
	endDate = datetime.now(),
	statusId = None,
	invoice_list = None,
	rp_acc_user = None,
	DivId = None,
	notDivId = None,
	invoice_models = None,
):
	if not invoice_models:
		invoice_filtering = {
			"GCRecord": None
		}
		if statusId:
			invoice_filtering["InvStatId"] = statusId
		if rp_acc_user:
			invoice_filtering["RpAccId"] = rp_acc_user.RpAccId

		invoice_models = []
		if not invoice_list:
			order_invoices = Order_inv.query\
				.filter_by(**invoice_filtering)
			if DivId:
				order_invoices = order_invoices.filter_by(DivId = DivId)
			if notDivId:
				order_invoices = order_invoices.filter(Order_inv.DivId != notDivId)

			if startDate:
				if (type(startDate) != datetime):
					startDate = dateutil.parser.parse(startDate)
					startDate = datetime.date(startDate)
				if (type(endDate) != datetime):
					endDate = dateutil.parser.parse(endDate)
					endDate = datetime.date(endDate)
				order_invoices = order_invoices\
					.filter(and_(
						extract('year',Order_inv.OInvDate).between(startDate.year,endDate.year),\
						extract('month',Order_inv.OInvDate).between(startDate.month,endDate.month),\
						extract('day',Order_inv.OInvDate).between(startDate.day,endDate.day)))

			order_invoices = order_invoices\
				.order_by(Order_inv.OInvDate.desc())\
				.options(
					joinedload(Order_inv.rp_acc),
					joinedload(Order_inv.inv_status),
					joinedload(Order_inv.company),
					joinedload(Order_inv.warehouse),
					joinedload(Order_inv.division),
					joinedload(Order_inv.Order_inv_line)\
						.options(
							joinedload(Order_inv_line.resource)
						))\
				.all()

			for order_inv in order_invoices:
				invoice_models.append(order_inv)

		elif invoice_list:
			for invoice_index in invoice_list:
				OInvRegNo = invoice_index["OInvRegNo"]
				invoice_filtering["OInvRegNo"] = OInvRegNo
				order_inv = Order_inv.query\
					.filter_by(**invoice_filtering).first()
				if order_inv:
					invoice_models.append(order_inv)

	return invoice_models
