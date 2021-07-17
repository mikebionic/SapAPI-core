from main_pack.config import Config
from sqlalchemy.orm import joinedload

from main_pack.models import (
	Order_inv,
	Order_inv_line,
)

from main_pack.api.commerce.commerce_utils import apiResourceInfo

from main_pack.base.languageMethods import dataLangSelector

# colorful bootstrap status configurations library
from main_pack.base.invoiceMethods import getInvStatusUi


# !!! TODO: Update this to use single query and get rid of list iter query
def UiOInvData(orders_list):
	data = []

	for order in orders_list:
		orderInv = Order_inv.query\
			.options(
				joinedload(Order_inv.rp_acc),
				joinedload(Order_inv.user),
				joinedload(Order_inv.order_inv_type),
				joinedload(Order_inv.inv_status),
				joinedload(Order_inv.currency)
			)\
			.get(order["OInvId"])
		
		order_inv_data = orderInv.to_json_api()

		order_inv_data["Rp_acc"] = orderInv.rp_acc.to_json_api() if orderInv.rp_acc else {}
		order_inv_data["User"] = orderInv.user.to_json_api() if orderInv.user else {}
		order_inv_data["InvStatus"] = dataLangSelector(orderInv.inv_status.to_json_api()) if orderInv.inv_status else {}
		order_inv_data["OInvType"] = dataLangSelector(orderInv.order_inv_type.to_json_api()) if orderInv.order_inv_type else {}
		order_inv_data["Currency"] = dataLangSelector(orderInv.currency.to_json_api()) if orderInv.currency else {}
		order_inv_data["CurrencyCode"] = orderInv.currency.CurrencyCode if orderInv.currency else Config.MAIN_CURRENCY_CODE
		order_inv_data["StatusUI"] = getInvStatusUi(orderInv.InvStatId)

		data.append(order_inv_data)

	res = {
		"orderInvoices":data,
	}

	return res


def UiOInvLineData(
	order_lines_list,
	detailed_resource = False
):
	data = []

	for order_line in order_lines_list:
		orderInvLine = Order_inv_line.query\
			.options(
				joinedload(Order_inv_line.resource),	
				joinedload(Order_inv_line.currency)
			)\
			.get(order_line["OInvLineId"])

		orderInvLineList = orderInvLine.to_json_api()
		resource_model = orderInvLine.resource

		orderInvLineList["CurrencyCode"] = orderInvLine.currency.CurrencyCode if orderInvLine.currency else Config.MAIN_CURRENCY_CODE
		orderInvLineList["Currency"] = dataLangSelector(orderInvLine.currency.to_json_api()) if orderInvLine.currency else {}

		if detailed_resource:
			orderInvLineList["Resource"] = apiResourceInfo(
				single_object = 1,
				showInactive = 1,
				resource_list = [{"ResId": resource_model.ResId}],
				avoidQtyCheckup = 1,
				showNullPrice = 1
			)["data"]

		else:
			orderInvLineList["Resource"] = resource_model.to_json_api() if resource_model else ''

		data.append(orderInvLineList)

	res = {
		"orderInvLines":data,
	}
	return res


def addOInvLineDict(req):
	OInvId = req.get('OInvId')
	UnitId = req.get('UnitId')
	CurrencyId = req.get('CurrencyId')
	ResId = req.get('ResId')
	LastVendorId = req.get('LastVendorId')
	OInvLineDesc = req.get('OInvLineDesc')
	OInvLineAmount = req.get('OInvLineAmount')
	OInvLinePrice = req.get('OInvLinePrice')
	OInvLineTotal = req.get('OInvLineTotal')
	OInvLineExpenseAmount = req.get('OInvLineExpenseAmount')
	OInvLineTaxAmount = req.get('OInvLineTaxAmount')
	OInvLineDiscAmount = req.get('OInvLineDiscAmount')
	OInvLineFTotal = req.get('OInvLineFTotal')
	OInvLineDate = req.get('OInvLineDate')
	ExcRateValue = req.get('ExcRateValue')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	orderInvLine = {
		"OInvId": OInvId,
		"UnitId": UnitId,
		"CurrencyId": CurrencyId,
		"ResId": ResId,
		"LastVendorId": LastVendorId,
		"OInvLineDesc": OInvLineDesc,
		"OInvLineAmount": OInvLineAmount,
		"OInvLinePrice": OInvLinePrice,
		"OInvLineTotal": OInvLineTotal,
		"OInvLineExpenseAmount": OInvLineExpenseAmount,
		"OInvLineTaxAmount": OInvLineTaxAmount,
		"OInvLineDiscAmount": OInvLineDiscAmount,
		"OInvLineFTotal": OInvLineFTotal,
		"OInvLineDate": OInvLineDate,
		"ExcRateValue": ExcRateValue,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	return orderInvLine

def addOInvDict(req):
	OInvTypeId = req.get('OInvTypeId')
	InvStatId = req.get('InvStatId')
	CurrencyId = req.get('CurrencyId')
	RpAccId = req.get('RpAccId')
	CId = req.get('CId')
	DivId = req.get('DivId')
	WhId = req.get('WhId')
	WpId = req.get('WpId')
	EmpId = req.get('EmpId')
	OInvRegNo = req.get('OInvRegNo')
	OInvDesc = req.get('OInvDesc')
	OInvDate = req.get('OInvDate')
	OInvTotal = req.get('OInvTotal')
	OInvExpenseAmount = req.get('OInvExpenseAmount')
	OInvTaxAmount = req.get('OInvTaxAmount')
	OInvDiscountAmount = req.get('OInvDiscountAmount')
	OInvFTotal = req.get('OInvFTotal')
	OInvFTotalInWrite = req.get('OInvFTotalInWrite')
	OInvModifyCount = req.get('OInvModifyCount')
	OInvPrintCount = req.get('OInvPrintCount')
	OInvCreditDays = req.get('OInvCreditDays')
	OInvCreditDesc = req.get('OInvCreditDesc')
	AddInf1 = req.get('AddInf1')
	AddInf2 = req.get('AddInf2')
	AddInf3 = req.get('AddInf3')
	AddInf4 = req.get('AddInf4')
	AddInf5 = req.get('AddInf5')
	AddInf6 = req.get('AddInf6')
	CreatedDate = req.get('CreatedDate')
	ModifiedDate = req.get('ModifiedDate')
	CreatedUId = req.get('CreatedUId')
	ModifiedUId = req.get('ModifiedUId')
	GCRecord = req.get('GCRecord')

	orderInv = {
		"OInvTypeId": OInvTypeId,
		"InvStatId": InvStatId,
		"CurrencyId": CurrencyId,
		"RpAccId": RpAccId,
		"CId": CId,
		"DivId": DivId,
		"WhId": WhId,
		"WpId": WpId,
		"EmpId": EmpId,
		"OInvRegNo": OInvRegNo,
		"OInvDesc": OInvDesc,
		"OInvDate": OInvDate,
		"OInvTotal": OInvTotal,
		"OInvExpenseAmount": OInvExpenseAmount,
		"OInvTaxAmount": OInvTaxAmount,
		"OInvDiscountAmount": OInvDiscountAmount,
		"OInvFTotal": OInvFTotal,
		"OInvFTotalInWrite": OInvFTotalInWrite,
		"OInvModifyCount": OInvModifyCount,
		"OInvPrintCount": OInvPrintCount,
		"OInvCreditDays": OInvCreditDays,
		"OInvCreditDesc": OInvCreditDesc,
		"AddInf1": AddInf1,
		"AddInf2": AddInf2,
		"AddInf3": AddInf3,
		"AddInf4": AddInf4,
		"AddInf5": AddInf5,
		"AddInf6": AddInf6,
		"CreatedDate": CreatedDate,
		"ModifiedDate": ModifiedDate,
		"CreatedUId": CreatedUId,
		"ModifiedUId": ModifiedUId,
		"GCRecord": GCRecord
	}
	return orderInv