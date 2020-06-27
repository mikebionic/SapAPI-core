from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck
from main_pack.base.imageMethods import save_image,dirHandler
# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,Sale_agr_res_price,Res_discount)

# for invoices
from main_pack.models.commerce.models import (Inv_line,Inv_line_det,Inv_line_det_type,
	Inv_status,Inv_type,Invoice,Order_inv,Order_inv_line,Order_inv_type)
from main_pack.models.base.models import Currency
from main_pack.models.commerce.models import Resource

from main_pack.models.base.models import Company,Division
from main_pack.models.users.models import Rp_acc
from main_pack.base.languageMethods import dataLangSelector
from main_pack.base.invoiceMethods import getInvStatusUi

from sqlalchemy import and_

def UiOInvData(orders_list):
	data = []

	currencies = Currency.query\
		.filter(Currency.GCRecord=='' or Currency.GCRecord==None).all()
	inv_statuses = Inv_status.query\
		.filter(Inv_status.GCRecord=='' or Inv_status.GCRecord==None).all()
	orderInvTypes = Order_inv_type.query\
		.filter(Order_inv_type.GCRecord=='' or Order_inv_type.GCRecord==None).all()
	rpAccs = Rp_acc.query\
		.filter(Rp_acc.GCRecord=='' or Rp_acc.GCRecord==None).all()

	for order in orders_list:
		orderInv = Order_inv.query.get(order["OInvId"])
		orderInvList = orderInv.to_json_api()
		
		List_RpAccs = [rpAcc.to_json_api() for rpAcc in rpAccs if rpAcc.RpAccId==orderInv.RpAccId]
		List_InvStatuses = [inv_status.to_json_api() for inv_status in inv_statuses if inv_status.InvStatId==orderInv.InvStatId]
		List_OInvTypes = [orderInvType.to_json_api() for orderInvType in orderInvTypes if orderInvType.OInvTypeId==orderInv.OInvTypeId]
		List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId==orderInv.CurrencyId]

		orderInvList["Rp_acc"] = List_RpAccs[0] if List_RpAccs else ''
		orderInvList["InvStatus"] = dataLangSelector(List_InvStatuses[0]) if List_InvStatuses else ''
		orderInvList["OInvType"] = dataLangSelector(List_OInvTypes[0]) if List_OInvTypes else ''
		orderInvList["Currency"] = dataLangSelector(List_Currencies[0]) if List_Currencies else ''
		orderInvList["StatusUI"] = getInvStatusUi(orderInv.InvStatId)
		data.append(orderInvList)
	res = {
		"orderInvoices":data,
	}
	return res


def UiOInvLineData(order_lines_list):
	data = []

	units = Unit.query\
		.filter(Currency.GCRecord=='' or Currency.GCRecord==None).all()
	currencies = Currency.query\
		.filter(Currency.GCRecord=='' or Currency.GCRecord==None).all()
	orderInvTypes = Order_inv_type.query\
		.filter(Order_inv_type.GCRecord=='' or Order_inv_type.GCRecord==None).all()

	print(order_lines_list)
	for order_line in order_lines_list:
		orderInvLine = Order_inv_line.query.get(order_line["OInvLineId"])
		orderInvLineList = orderInvLine.to_json_api()
		
		resource = Resource.query\
			.filter(and_(Resource.GCRecord=='' or Resource.GCRecord==None),Resource.ResId==orderInvLine.ResId).first()
		
		List_Units = [unit.to_json_api() for unit in units if unit.UnitId==orderInvLine.UnitId]
		List_Currencies = [currency.to_json_api() for currency in currencies if currency.CurrencyId==orderInvLine.CurrencyId]

		orderInvLineList["Unit"] = dataLangSelector(List_Units[0]) if List_Units else ''
		orderInvLineList["Currency"] = dataLangSelector(List_Currencies[0]) if List_Currencies else ''
		orderInvLineList["Resource"] = resource.to_json_api() if resource else ''

		data.append(orderInvLineList)
	res = {
		"orderInvLines":data,
	}
	return res

def invStatusesSelectData():
	invStatusesList=[]
	inv_statuses = Inv_status.query\
	.filter(Inv_status.GCRecord=='' or Inv_status.GCRecord==None).all()
	for inv_status in inv_statuses:
		status = dataLangSelector(inv_status.to_json_api())
		obj=(status['InvStatId'],status['InvStatName'])
		invStatusesList.append(obj)
	return invStatusesList


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
		'OInvId':OInvId,
		'UnitId':UnitId,
		'CurrencyId':CurrencyId,
		'ResId':ResId,
		'LastVendorId':LastVendorId,
		'OInvLineDesc':OInvLineDesc,
		'OInvLineAmount':OInvLineAmount,
		'OInvLinePrice':OInvLinePrice,
		'OInvLineTotal':OInvLineTotal,
		'OInvLineExpenseAmount':OInvLineExpenseAmount,
		'OInvLineTaxAmount':OInvLineTaxAmount,
		'OInvLineDiscAmount':OInvLineDiscAmount,
		'OInvLineFTotal':OInvLineFTotal,
		'OInvLineDate':OInvLineDate,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
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
		'OInvTypeId':OInvTypeId,
		'InvStatId':InvStatId,
		'CurrencyId':CurrencyId,
		'RpAccId':RpAccId,
		'CId':CId,
		'DivId':DivId,
		'WhId':WhId,
		'WpId':WpId,
		'EmpId':EmpId,
		'OInvRegNo':OInvRegNo,
		'OInvDesc':OInvDesc,
		'OInvDate':OInvDate,
		'OInvTotal':OInvTotal,
		'OInvExpenseAmount':OInvExpenseAmount,
		'OInvTaxAmount':OInvTaxAmount,
		'OInvDiscountAmount':OInvDiscountAmount,
		'OInvFTotal':OInvFTotal,
		'OInvFTotalInWrite':OInvFTotalInWrite,
		'OInvModifyCount':OInvModifyCount,
		'OInvPrintCount':OInvPrintCount,
		'OInvCreditDays':OInvCreditDays,
		'OInvCreditDesc':OInvCreditDesc,
		'AddInf1':AddInf1,
		'AddInf2':AddInf2,
		'AddInf3':AddInf3,
		'AddInf4':AddInf4,
		'AddInf5':AddInf5,
		'AddInf6':AddInf6,
		'CreatedDate':CreatedDate,
		'ModifiedDate':ModifiedDate,
		'CreatedUId':CreatedUId,
		'ModifiedUId':ModifiedUId,
		'GCRecord':GCRecord
	}
	return orderInv