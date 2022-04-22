from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from main_pack import db
from main_pack.models import AddInf, BaseModel


class Warehouse(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_warehouse"
	WhId = db.Column("WhId",db.Integer,nullable=False,primary_key=True)
	WhGuid = db.Column("WhGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	WhTypeId = db.Column("WhTypeId",db.Integer,db.ForeignKey("tbl_dk_wh_type.WhTypeId"))
	WhName = db.Column("WhName",db.String(100),nullable=False)
	WhDesc = db.Column("WhDesc",db.String(500))
	Res_transaction = db.relationship("Res_transaction",backref='warehouse',lazy=True)
	Invoice = db.relationship("Invoice",backref='warehouse',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='warehouse',lazy=True)
	Res_total = db.relationship("Res_total",backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",foreign_keys='Res_trans_inv.WhIdIn',backref='warehouse',lazy=True)
	Res_trans_inv = db.relationship("Res_trans_inv",foreign_keys='Res_trans_inv.WhIdOut',backref='warehouse',lazy=True)
	Production = db.relationship("Production",foreign_keys='Production.WhIdIn',backref='warehouse',lazy=True)
	Production = db.relationship("Production",foreign_keys='Production.WhIdOut',backref='warehouse',lazy=True)
	Wh_inv_line = db.relationship("Wh_inv_line",backref='warehouse',lazy=True)
	Wh_invoice = db.relationship("Wh_invoice",backref='warehouse',lazy=True)

	def to_json_api(self):
		data = {
			"WhId": self.WhId,
			"WhGuid": self.WhGuid,
			"CId": self.CId,
			"DivId": self.DivId,
			"UsageStatusId": self.UsageStatusId,
			"WhTypeId": self.WhTypeId,
			"WhName": self.WhName,
			"WhDesc": self.WhDesc,
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data

class Wh_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_wh_type"
	WhTypeId = db.Column("WhTypeId",db.Integer,nullable=False,primary_key=True)
	WhTypeGuid = db.Column("WhTypeGuid",UUID(as_uuid=True),unique=True)
	WhTypeName_tkTM = db.Column("WhTypeName_tkTM",db.String(100),nullable=False)
	WhTypeDesc_tkTM = db.Column("WhTypeDesc_tkTM",db.String(100))
	WhTypeName_enUS = db.Column("WhTypeName_enUS",db.String(100))
	WhTypeDesc_enUS = db.Column("WhTypeDesc_enUS",db.String(100))
	WhTypeName_ruRU = db.Column("WhTypeName_ruRU",db.String(100))
	WhTypeDesc_ruRU = db.Column("WhTypeDesc_ruRU",db.String(100))
	Warehouse = db.relationship("Warehouse",backref='wh_type',lazy=True)

	def to_json_api(self):
		data = {
			"WhTypeId": self.WhTypeId,
			"WhTypeGuid": self.WhTypeGuid,
			"WhTypeName_tkTM": self.WhTypeName_tkTM,
			"WhTypeDesc_tkTM": self.WhTypeDesc_tkTM,
			"WhTypeName_enUS": self.WhTypeName_enUS,
			"WhTypeDesc_enUS": self.WhTypeDesc_enUS,
			"WhTypeName_ruRU": self.WhTypeName_ruRU,
			"WhTypeDesc_ruRU": self.WhTypeDesc_ruRU,
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data


class Wh_inv_type(BaseModel, db.Model):
	__tablename__ = "tbl_dk_wh_inv_type"
	WhInvTypeId = db.Column("WhInvTypeId",db.Integer,nullable=False,primary_key=True)
	WhInvTypeGuid = db.Column("WhInvTypeGuid",UUID(as_uuid=True),unique=True)
	WhInvTypeName_tkTM = db.Column("WhInvTypeName_tkTM",db.String(100),nullable=False)
	WhInvTypeDesc_tkTM = db.Column("WhInvTypeDesc_tkTM",db.String(500))
	WhInvTypeName_enUS = db.Column("WhInvTypeName_enUS",db.String(100),nullable=False)
	WhInvTypeDesc_enUS = db.Column("WhInvTypeDesc_enUS",db.String(500))
	WhInvTypeName_ruRU = db.Column("WhInvTypeName_ruRU",db.String(100),nullable=False)
	WhInvTypeDesc_ruRU = db.Column("WhInvTypeDesc_ruRU",db.String(500))
	Wh_invoice = db.relationship("Wh_invoice",backref='wh_inv_type',lazy=True)

	def to_json_api(self):
		data = {
			"WhInvTypeId": self.WhInvTypeId,
			"WhInvTypeGuid": self.WhInvTypeGuid,
			"WhInvTypeName_tkTM": self.WhInvTypeName_tkTM,
			"WhInvTypeDesc_tkTM": self.WhInvTypeDesc_tkTM,
			"WhInvTypeName_enUS": self.WhInvTypeName_enUS,
			"WhInvTypeDesc_enUS": self.WhInvTypeDesc_enUS,
			"WhInvTypeName_ruRU": self.WhInvTypeName_ruRU,
			"WhInvTypeDesc_ruRU": self.WhInvTypeDesc_ruRU,
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data

class Wh_invoice(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_wh_invoice"
	WhInvId = db.Column("WhInvId",db.Integer,nullable=False,primary_key=True)
	WhInvGuid = db.Column("WhInvGuid",UUID(as_uuid=True),unique=True)
	WhInvTypeId = db.Column("WhInvTypeId",db.Integer,db.ForeignKey("tbl_dk_wh_inv_type.WhInvTypeId"))
	InvTypeId = db.Column("InvTypeId",db.Integer,db.ForeignKey("tbl_dk_inv_type.InvTypeId"))
	PtId = db.Column("PtId",db.Integer,db.ForeignKey("tbl_dk_payment_type.PtId"))
	PmId = db.Column("PmId",db.Integer,db.ForeignKey("tbl_dk_payment_method.PmId"))
	InvStatId = db.Column("InvStatId",db.Integer,db.ForeignKey("tbl_dk_inv_status.InvStatId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	WhInvRegNo = db.Column("WhInvRegNo",db.String(100),nullable=False,unique=True)
	WhInvDesc = db.Column("WhInvDesc",db.String(500))
	WhInvDate = db.Column("WhInvDate",db.DateTime,default=datetime.now)
	WhInvTotal = db.Column("WhInvTotal",db.Float,default=0.0)
	WhInvExpenseAmount = db.Column("WhInvExpenseAmount",db.Float,default=0.0)
	WhInvTaxAmount = db.Column("WhInvTaxAmount",db.Float,default=0.0)
	WhInvDiscountAmount = db.Column("WhInvDiscountAmount",db.Float,default=0.0)
	WhInvFTotal = db.Column("WhInvFTotal",db.Float,default=0.0)
	WhInvFTotalInWrite = db.Column("WhInvFTotalInWrite",db.String(100))
	WhInvModifyCount = db.Column("WhInvModifyCount",db.Integer,default=0)
	WhInvPrintCount = db.Column("WhInvPrintCount",db.Integer,default=0)
	WhInvCreditDays = db.Column("WhInvCreditDays",db.Integer,default=0)
	WhInvCreditDesc = db.Column("WhInvCreditDesc",db.String(100))
	WhInvLatitude = db.Column("WhInvLatitude",db.Float,default=0.0)
	WhInvLongitude = db.Column("WhInvLongitude",db.Float,default=0.0)
	PaymStatusId = db.Column("PaymStatusId",db.Integer,db.ForeignKey("tbl_dk_payment_status.PaymStatusId"))
	PaymCode = db.Column("PaymCode",db.String(500))
	PaymDesc = db.Column("PaymDesc",db.String(500))
	WhInvPaymAmount = db.Column("WhInvPaymAmount",db.Float,default=0.0)
	Wh_inv_line = db.relationship("Wh_inv_line",backref='wh_invoice',lazy=True)

	def to_json_api(self):
		data = {
			"WhInvId": self.WhInvId,
			"WhInvGuid": self.WhInvGuid,
			"WhInvTypeId": self.WhInvTypeId,
			"InvTypeId": self.InvTypeId,
			"PtId": self.PtId,
			"PmId": self.PmId,
			"InvStatId": self.InvStatId,
			"CurrencyId": self.CurrencyId,
			"RpAccId": self.RpAccId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhId": self.WhId,
			"WpId": self.WpId,
			"EmpId": self.EmpId,
			"UId": self.UId,
			"WhInvRegNo": self.WhInvRegNo,
			"WhInvDesc": self.WhInvDesc,
			"WhInvDate": self.WhInvDate,
			"WhInvTotal": self.WhInvTotal,
			"WhInvExpenseAmount": self.WhInvExpenseAmount,
			"WhInvTaxAmount": self.WhInvTaxAmount,
			"WhInvDiscountAmount": self.WhInvDiscountAmount,
			"WhInvFTotal": self.WhInvFTotal,
			"WhInvFTotalInWrite": self.WhInvFTotalInWrite,
			"WhInvModifyCount": self.WhInvModifyCount,
			"WhInvPrintCount": self.WhInvPrintCount,
			"WhInvCreditDays": self.WhInvCreditDays,
			"WhInvCreditDesc": self.WhInvCreditDesc,
			"WhInvLatitude": self.WhInvLatitude,
			"WhInvLongitude": self.WhInvLongitude,
			"PaymStatusId": self.PaymStatusId,
			"PaymCode": self.PaymCode,
			"PaymDesc": self.PaymDesc,
			"WhInvPaymAmount": self.WhInvPaymAmount,
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data


class Wh_inv_line(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_wh_inv_line"
	WhInvLineId = db.Column("WhInvLineId",db.Integer,nullable=False,primary_key=True)
	WhInvLineGuid = db.Column("WhInvLineGuid",UUID(as_uuid=True),unique=True)
	WhInvId = db.Column("WhInvId",db.Integer,db.ForeignKey("tbl_dk_wh_invoice.WhInvId"))
	InvLineId = db.Column("InvLineId",db.Integer,db.ForeignKey("tbl_dk_inv_line.InvLineId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column("LastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WhTransTypeId = db.Column("WhTransTypeId",db.Integer) #?
	WhInvLineRegNo = db.Column("WhInvLineRegNo",db.String(100))
	WhInvLineDesc = db.Column("WhInvLineDesc",db.String(500))
	WhInvLineAmount = db.Column("WhInvLineAmount",db.Float,default=0.0)
	WhInvLinePrice = db.Column("WhInvLinePrice",db.Float,default=0.0)
	WhInvLineTotal = db.Column("WhInvLineTotal",db.Float,default=0.0)
	WhInvLineExpenseAmount = db.Column("WhInvLineExpenseAmount",db.Float,default=0.0)
	WhInvLineTaxAmount = db.Column("WhInvLineTaxAmount",db.Float,default=0.0)
	WhInvLineDiscAmount = db.Column("WhInvLineDiscAmount",db.Float,default=0.0)
	WhInvLineFTotal = db.Column("WhInvLineFTotal",db.Float,default=0.0)
	ExcRateValue = db.Column("ExcRateValue",db.Float,default=0.0)
	WhInvLineDate = db.Column("WhInvLineDate",db.DateTime,default=datetime.now)
	Wh_inv_line_det = db.relationship("Wh_inv_line_det",backref='wh_inv_line',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='wh_inv_line',lazy=True)


	def to_json_api(self):
		data = {
			"WhInvLineId": self.WhInvLineId,
			"WhInvLineGuid": self.WhInvLineGuid,
			"WhInvId": self.WhInvId,
			"InvLineId": self.InvLineId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"LastVendorId": self.LastVendorId,
			"WhId": self.WhId,
			"WhTransTypeId": self.WhTransTypeId,
			"WhInvLineRegNo": self.WhInvLineRegNo,
			"WhInvLineDesc": self.WhInvLineDesc,
			"WhInvLineAmount": self.WhInvLineAmount,
			"WhInvLinePrice": self.WhInvLinePrice,
			"WhInvLineTotal": self.WhInvLineTotal,
			"WhInvLineExpenseAmount": self.WhInvLineExpenseAmount,
			"WhInvLineTaxAmount": self.WhInvLineTaxAmount,
			"WhInvLineDiscAmount": self.WhInvLineDiscAmount,
			"WhInvLineFTotal": self.WhInvLineFTotal,
			"ExcRateValue": self.ExcRateValue,
			"WhInvLineDate": self.WhInvLineDate,
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data


class Wh_inv_line_det(BaseModel, db.Model):
	__tablename__ = "tbl_dk_wh_inv_line_det"
	WhInvLineDetId = db.Column("WhInvLineDetId",db.Integer,nullable=False,primary_key=True)
	WhInvLineDetGuid = db.Column("WhInvLineDetGuid",UUID(as_uuid=True),unique=True)
	WhInvLineId = db.Column("WhInvLineId",db.Integer,db.ForeignKey("tbl_dk_wh_inv_line.WhInvLineId"))
	InvLineDetTypeId = db.Column("InvLineDetTypeId",db.Integer,db.ForeignKey("tbl_dk_inv_line_det_type.InvLineDetTypeId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	WhInvLineDetResSN = db.Column("WhInvLineDetResSN",db.String(100))
	WhInvLineDetSLStartDate = db.Column("WhInvLineDetSLStartDate",db.DateTime)
	WhInvLineDetSLEndDate = db.Column("WhInvLineDetSLEndDate",db.DateTime)
	WhInvLineDetAmount = db.Column("WhInvLineDetAmount",db.Float)
	WhInvLineDetAmountBalance = db.Column("WhInvLineDetAmountBalance",db.Float)

	def to_json_api(self):
		data = {
			"WhInvLineDetId": self.WhInvLineDetId,
			"WhInvLineDetGuid": self.WhInvLineDetGuid,
			"WhInvLineId": self.WhInvLineId,
			"InvLineDetTypeId": self.InvLineDetTypeId,
			"ResId": self.ResId,
			"WhInvLineDetResSN": self.WhInvLineDetResSN,
			"WhInvLineDetSLStartDate": self.WhInvLineDetSLStartDate,
			"WhInvLineDetSLEndDate": self.WhInvLineDetSLEndDate,
			"WhInvLineDetAmount": self.WhInvLineDetAmount,
			"WhInvLineDetAmountBalance": self.WhInvLineDetAmountBalance,
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data