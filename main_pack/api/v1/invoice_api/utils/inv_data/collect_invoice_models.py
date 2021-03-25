# -*- coding: utf-8 -*-
from datetime import datetime

import dateutil.parser
from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload

from main_pack.models.commerce.models import Invoice, Inv_line

def collect_invoice_models(
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
		if invoice_list is None:
			invoices_query = Invoice.query\
				.filter_by(**invoice_filtering)
			if DivId:
				invoices_query = invoices_query.filter_by(DivId = DivId)
			if notDivId:
				invoices_query = invoices_query.filter(Invoice.DivId != notDivId)

			if startDate:
				if (type(startDate) != datetime):
					startDate = dateutil.parser.parse(startDate)
					startDate = datetime.date(startDate)
				if (type(endDate) != datetime):
					endDate = dateutil.parser.parse(endDate)
					endDate = datetime.date(endDate)
				invoices_query = invoices_query\
					.filter(and_(
						extract('year',Invoice.InvDate).between(startDate.year,endDate.year),\
						extract('month',Invoice.InvDate).between(startDate.month,endDate.month),\
						extract('day',Invoice.InvDate).between(startDate.day,endDate.day)))

			invoices_query = invoices_query\
				.order_by(Invoice.InvDate.desc())\
				.options(
					joinedload(Invoice.rp_acc),
					joinedload(Invoice.inv_status),
					joinedload(Invoice.company),
					joinedload(Invoice.warehouse),
					joinedload(Invoice.division),
					joinedload(Invoice.Inv_line)\
						.options(
							joinedload(Inv_line.resource)
						))\
				.all()

			for invoice_object in invoices_query:
				invoice_models.append(invoice_object)

		elif invoice_list:
			for invoice_index in invoice_list:
				OInvRegNo = invoice_index["OInvRegNo"]
				invoice_filtering["OInvRegNo"] = OInvRegNo
				invoice_object = Invoice.query\
					.filter_by(**invoice_filtering).first()
				if invoice_object:
					invoice_models.append(invoice_object)

	return invoice_models