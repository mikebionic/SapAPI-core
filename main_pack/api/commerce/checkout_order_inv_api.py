# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response, session
import requests, json
import uuid
from sqlalchemy.orm import joinedload
from datetime import datetime
import decimal

from main_pack import db
from main_pack.config import Config
from . import api

from main_pack.models import User
from main_pack.api.auth.utils import token_required

# Orders
from main_pack.models import Order_inv, Order_inv_line, Work_period
from .utils import addOrderInvDict, addOrderInvLineDict
from main_pack.base.invoiceMethods import get_order_error_type
from main_pack.base.apiMethods import checkApiResponseStatus
# / Orders /

from main_pack.key_generator.utils import generate, makeRegNo, Pred_reg_num
from main_pack.api.base.validators import request_is_json

# Resource models and operations
from  main_pack.models import Warehouse, Currency
from main_pack.models import (
	Resource,
	Res_price,
	Res_total,
	Res_price_group,
	Exc_rate
)
from main_pack.base.invoiceMethods import totalQtySubstitution
from main_pack.base.priceMethods import calculatePriceByGroup, price_currency_conversion
from main_pack.base.num2text import num2text, price2text
# / Resource models and operations /


@api.route("/checkout-sale-order-inv/",methods=['POST'])
@token_required
@request_is_json(request)
def api_checkout_sale_order_invoices(user):
	model_type = user['model_type']
	current_user = user['current_user']

	currencies = Currency.query.filter_by(GCRecord = None).all()
	res_price_groups = Res_price_group.query.filter_by(GCRecord = None).all()
	exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()

	work_period = Work_period.query\
		.filter_by(GCRecord = None, WpIsDefault = True)\
		.first()
	# !!! current user is rp_acc if type is rp_acc
	if model_type == "rp_acc":
		name = current_user.RpAccUName
		RpAccId = current_user.RpAccId
		DivId = current_user.DivId
		CId = current_user.CId

		warehouse = Warehouse.query\
			.filter_by(DivId = DivId, GCRecord = None)\
			.order_by(Warehouse.WhId.asc())\
			.first()
		WhId = warehouse.WhId if warehouse else None

		# get the seller's user information of a specific rp_acc
		user = current_user.user
		if user is None:
			# try to find the rp_acc registered user if no seller specified
			user = User.query\
				.filter_by(GCRecord = None, UTypeId = 1)\
				.first()

	ResPriceGroupId = Config.DEFAULT_RES_PRICE_GROUP_ID if Config.DEFAULT_RES_PRICE_GROUP_ID > 0 else None
	if current_user:
		if (model_type != "device"):
			ResPriceGroupId = current_user.ResPriceGroupId if current_user.ResPriceGroupId else None
		else:
			ResPriceGroupId = current_user.user.ResPriceGroupId if current_user.user else None

	elif "ResPriceGroupId" in session:
		ResPriceGroupId = session["ResPriceGroupId"]

	req = request.get_json()
	req['orderInv']['OInvGuid'] = str(uuid.uuid4())
	order_invoice = addOrderInvDict(req['orderInv'])
	try:
		orderRegNo = req['orderInv']['OInvRegNo']
		InvStatId = req['orderInv']['InvStatId']
		reg_num_pred_exists = None

		if not req['orderInv']['OrderInvLines']:
			raise Exception

		if not orderRegNo:
			try:
				reg_num = generate(UId=user.UId,RegNumTypeName='sale_order_invoice_code')
				orderRegNo = makeRegNo(
					user.UShortName,
					reg_num.RegNumPrefix,
					reg_num.RegNumLastNum+1,
					'',
					True,
					RegNumTypeName='sale_order_invoice_code',
				)
			except Exception as ex:
				print(f"{datetime.now()} | Checkout OInv Exception: {ex}. Couldn't generate RegNo using User's credentials")
				# use device model and other info
				orderRegNo = str(datetime.now().timestamp())

		else:
			reg_num_pred_exists = Pred_reg_num.query\
				.filter_by(GCRecord = None, RegNum = orderRegNo).first()
			if not reg_num_pred_exists:
				raise Exception

		###### order inv setup ######
		order_invoice["OInvRegNo"] = orderRegNo
		order_invoice["InvStatId"] = 1
		order_invoice["OInvTypeId"] = 2
		order_invoice["WpId"] = work_period.WpId
		order_invoice["WhId"] = WhId
		order_invoice["DivId"] = DivId
		order_invoice["CId"] = CId
		order_invoice["UId"] = user.UId
		if InvStatId == 13:
			order_invoice["InvStatId"] = InvStatId

		# default currency is 1 TMT of not specified
		# !!! TODO: add currency validation for security
		if not order_invoice["CurrencyId"]:
			order_invoice["CurrencyId"] = 1
		order_invoice["RpAccId"] = RpAccId

		newOrderInv = Order_inv(**order_invoice)
		db.session.add(newOrderInv)

		order_inv_lines = []
		failed_order_inv_lines = []
		OInvTotal = 0
		OrderInvLines = req['orderInv']['OrderInvLines']
		for order_inv_line_req in OrderInvLines:
			try:
				# in case of errors, the error_type is provided
				error_type = 0
				order_inv_line_req['OInvLineGuid'] = str(uuid.uuid4())
				order_inv_line = addOrderInvLineDict(order_inv_line_req)
				# OInvLineRegNo generation
				try:
					reg_num = generate(UId=user.UId,RegNumTypeName='order_invoice_line_code')
					orderLineRegNo = makeRegNo(
						user.UShortName,
						reg_num.RegNumPrefix,
						reg_num.RegNumLastNum+1,
						'',
						True,
						RegNumTypeName='order_invoice_line_code',
					)
				except Exception as ex:
					print(f"{datetime.now()} | Checkout OInv Exception: {ex}. Couldn't generate RegNo using User's credentials")
					# use device model and other info
					orderLineRegNo = str(datetime.now().timestamp())
				order_inv_line["OInvLineRegNo"] = orderLineRegNo
				orderLineRegNo = None

				ResId = order_inv_line["ResId"]
				OInvLineAmount = int(order_inv_line["OInvLineAmount"])

				resource = Resource.query\
					.filter_by(GCRecord = None, ResId = ResId)\
					.options(joinedload(Resource.Res_price))\
					.first()

				if not resource:
					# type deleted or none
					error_type = 1
					raise Exception

				List_Res_price = calculatePriceByGroup(
					ResPriceGroupId = ResPriceGroupId,
					Res_price_dbModels = resource.Res_price,
					Res_pice_group_dbModels = res_price_groups)

				if not List_Res_price:
					raise Exception

				try:
					List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId == List_Res_price[0]["CurrencyId"]]
				except:
					List_Currencies = []

				this_priceValue = List_Res_price[0]["ResPriceValue"] if List_Res_price else 0.0
				this_currencyCode = List_Currencies[0]["CurrencyCode"] if List_Currencies else Config.MAIN_CURRENCY_CODE

				price_data = price_currency_conversion(
					priceValue = this_priceValue,
					from_currency = this_currencyCode,
					currencies_dbModel = currencies,
					exc_rates_dbModel = exc_rates)

				res_total = Res_total.query\
					.filter_by(GCRecord = None, ResId = ResId, WhId = WhId)\
					.first()
				totalSubstitutionResult = totalQtySubstitution(res_total.ResPendingTotalAmount,OInvLineAmount)

				if resource.UsageStatusId == 2:
					# resource unavailable or inactive
					error_type = 2
					raise Exception

				if totalSubstitutionResult["status"] == 0:
					# resource is empty or bad request with amount = -1
					error_type = 3
					raise Exception

				if order_inv_line["OInvLinePrice"] != price_data["ResPriceValue"]:
					error_type = 4
					raise Exception

				OInvLineAmount = totalSubstitutionResult["amount"]
				# ResPendingTotalAmount is decreased but not ResTotBalance
				res_total.ResPendingTotalAmount = totalSubstitutionResult["totalBalance"]
				############
				OInvLinePrice = float(price_data["ResPriceValue"])
				OInvLineTotal = OInvLinePrice * OInvLineAmount

				# add taxes and stuff later on
				OInvLineFTotal = OInvLineTotal

				###### inv line assignment ######
				order_inv_line["OInvLineAmount"] = decimal.Decimal(OInvLineAmount)
				order_inv_line["OInvLinePrice"] = decimal.Decimal(OInvLinePrice)
				order_inv_line["OInvLineTotal"] = decimal.Decimal(OInvLineTotal)
				order_inv_line["OInvLineFTotal"] = decimal.Decimal(OInvLineFTotal)
				order_inv_line["OInvId"] = newOrderInv.OInvId
				order_inv_line["UnitId"] = resource.UnitId
				order_inv_line["CurrencyId"] = price_data["CurrencyId"]

				# increment of Main Order Inv Total Price
				OInvTotal += OInvLineFTotal
				thisOInvLine = Order_inv_line(**order_inv_line)
				db.session.add(thisOInvLine)
				order_inv_lines.append(thisOInvLine.to_json_api())

				order_inv_line = None

			except Exception as ex:
				print(f"{datetime.now()} | Checkout OInv Line Exception: {ex} | Error type {error_type}")
				fail_info = {
					"data": order_inv_line_req,
					"error_type_id": error_type,
					"error_type_message": get_order_error_type(error_type)
				}
				failed_order_inv_lines.append(fail_info)

		###### final order assignment and processing ######
		# add taxes and stuff later on
		if failed_order_inv_lines:
			status = checkApiResponseStatus(order_inv_lines,failed_order_inv_lines)
			res = {
				"data": order_invoice,
				"successes": order_inv_lines,
				"fails": failed_order_inv_lines,
				"success_total": len(order_inv_lines),
				"fail_total": len(failed_order_inv_lines),
				"total": len(OrderInvLines)
			}
			status_code = 400
			for e in status:
				res[e] = status[e]

		else:
			OInvFTotal = OInvTotal
			OInvFTotalInWrite = price2text(
				OInvFTotal,
				Config.PRICE_2_TEXT_LANGUAGE,
				price_data["CurrencyCode"])

			newOrderInv.OInvTotal = decimal.Decimal(OInvTotal)
			newOrderInv.OInvFTotal = decimal.Decimal(OInvFTotal)
			newOrderInv.OInvFTotalInWrite = OInvFTotalInWrite

			if reg_num_pred_exists:
				db.session.delete(reg_num_pred_exists)

			db.session.commit()

			status = checkApiResponseStatus(order_inv_lines, failed_order_inv_lines)

			res = {
				"data": newOrderInv.to_json_api(),
				"successes": order_inv_lines,
				"fails": failed_order_inv_lines,
				"success_total": len(order_inv_lines),
				"fail_total": len(failed_order_inv_lines) or 0,
				"total": len(OrderInvLines)
			}

			# status_code = 201 if len(order_invoice) > 0 else 200
			status_code = 200
			for e in status:
				res[e] = status[e]

	except Exception as ex:
		print(f"{datetime.now()} | Checkout OInv Exception: {ex}")
		res = {
			"data": order_invoice,
			"message": "Failed to checkout order"
		}
		status_code = 400

	response = make_response(jsonify(res), status_code)

	return response


@api.route("/validate-order-inv-payment/",methods=['GET','POST'])
@token_required
@request_is_json(request)
def validate_order_inv_payment(user):
	current_user = user['current_user']
	RpAccId = current_user.RpAccId

	if request.method == 'POST':
		req = request.get_json()
		OInvRegNo = req["OInvRegNo"]
		OrderId = req["OrderId"]

		status = 0
		message = ''
		data = {}

		if OrderId:
			order_inv = Order_inv.query\
				.filter_by(
					RpAccId = RpAccId,
					OInvRegNo = OInvRegNo,
					GCRecord = None)\
				.first()

			if order_inv:
				# if order isn't already paid
				if order_inv.PaymStatusId != 2:
					try:
						r = requests.get(f"{Config.HALKBANK_PAYMENT_SERVICE_URL}?orderId={OrderId}&password={Config.HALKBANK_PAYMENT_SERVICE_PASSWORD}&userName={Config.HALKBANK_PAYMENT_SERVICE_USERNAME}", verify=False)
						response_json = json.loads(r.text)

						if (str(response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]) == str(Config.HALKBANK_PAYMENT_VALIDATION_VALUE)):
							PaymentAmount = int(response_json["Amount"])/100
							order_inv.OInvPaymAmount = PaymentAmount
							order_inv.InvStatId = 1
							if (PaymentAmount >= order_inv.OInvFTotal):
								order_inv.PaymStatusId = 2
							elif (PaymentAmount < order_inv.OInvFTotal and PaymentAmount > 0):
								order_inv.PaymStatusId = 3
							message = "Payment Validation: success"

						else:
							# invoice status = "Payment fail"
							# Payment status = "Not paid"
							order_inv.PaymStatusId = 1
							order_inv.OInvPaymAmount = 0
							order_inv.InvStatId = 14

							message = f"Payment Validation: failed (OrderStatus = {response_json[Config.HALKBANK_PAYMENT_VALIDATION_KEY]})"
							print(f"{datetime.now()} | {message}")

						order_inv.PaymCode = str(response_json)
						order_inv.PaymDesc = OrderId
						db.session.commit()
						data = response_json
						status = 1

					except Exception as ex:
						message = "Payment Validation: failed (Connection error)"
						print(f"{datetime.now()} | Payment Validation Exception: {ex}")

						req["message"] = message
						order_inv.PaymCode = str(req)
						order_inv.InvStatId = 14
						db.session.commit()

				else:
					message = "Already paid"

			else:
				message = "Payment Validation: failed (Order_inv is None)"
				print(f"{datetime.now()} | {message}")

		else:
			message = "Payment Validation: failed (OrderId is None)"
			print(f"{datetime.now()} | {message}")

		res = {
			"data": data,
			"message": message,
			"status": status,
			"total": len(data)
		}

		status_code = 200 if res["status"] == 0 else 201
		response = make_response(jsonify(res), status_code)

	return response