from main_pack.base.dataMethods import configureNulls,configureFloat,boolCheck
from main_pack.base.imageMethods import save_image,dirHandler
# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status,Res_category,Res_type,Res_maker
from main_pack.models.base.models import Company,Division,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)

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