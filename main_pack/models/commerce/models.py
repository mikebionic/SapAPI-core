from main_pack import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from flask_login import current_user
from main_pack.base.dataMethods import apiDataFormat,configureFloat
from main_pack.models.base.models import CreatedModifiedInfo, AddInf


class Barcode(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_barcode"
	BarcodeId = db.Column("BarcodeId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BarcodeVal = db.Column("BarcodeVal",db.String(100),nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"barcodeId": self.BarcodeId,
			"companyId": self.CId,
			"divisionId": self.DivId,
			"resId": self.ResId,
			"unitId": self.UnitId,
			"barcodeVal": self.BarcodeVal
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"BarcodeId": self.BarcodeId,
			"CId": self.CId,
			"DivId": self.DivId,
			"ResId": self.ResId,
			"UnitId": self.UnitId,
			"BarcodeVal": self.BarcodeVal,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Brand(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_brand"
	BrandId = db.Column("BrandId",db.Integer,nullable=False,primary_key=True)
	BrandName = db.Column("BrandName",db.String(100),nullable=False)
	BrandDesc = db.Column("BrandDesc",db.String(100),default="")
	BrandVisibleIndex = db.Column("BrandVisibleIndex",db.Integer,default=0)
	IsMain = db.Column("IsMain",db.Boolean,default=False)
	BrandLink1 = db.Column("BrandLink1",db.String(255))
	BrandLink2 = db.Column("BrandLink2",db.String(255))
	BrandLink3 = db.Column("BrandLink3",db.String(255))
	BrandLink4 = db.Column("BrandLink4",db.String(255))
	BrandLink5 = db.Column("BrandLink5",db.String(255))
	Resource = db.relationship("Resource",backref='brand',lazy=True)
	Image = db.relationship("Image",backref='brand',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"brandId": self.BrandId,
			"brandName": self.BrandName,
			"brandDesc": self.BrandDesc,
			"BrandLink1": self.BrandLink1,
			"BrandLink2": self.BrandLink2,
			"BrandLink3": self.BrandLink3,
			"BrandLink4": self.BrandLink4,
			"BrandLink5": self.BrandLink5
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"BrandId": self.BrandId,
			"BrandName": self.BrandName,
			"BrandDesc": self.BrandDesc,
			"BrandVisibleIndex": self.BrandVisibleIndex,
			"IsMain": self.IsMain,
			"BrandLink1": self.BrandLink1,
			"BrandLink2": self.BrandLink2,
			"BrandLink3": self.BrandLink3,
			"BrandLink4": self.BrandLink4,
			"BrandLink5": self.BrandLink5,			
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_color"
	ColorId = db.Column("ColorId",db.Integer,nullable=False,primary_key=True)
	ColorName = db.Column("ColorName",db.String(100),nullable=False)
	ColorDesc = db.Column("ColorDesc",db.String(500))
	ColorCode = db.Column("ColorCode",db.String(100))
	Res_color = db.relationship("Res_color",backref='color',lazy=True)
	Translations = db.relationship("Translations",backref='color',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"colorId": self.ColorId,
			"colorName": self.ColorName,
			"colorDesc": self.ColorDesc,
			"colorCode": self.ColorCode
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"ColorName": self.ColorName,
			"ColorDesc": self.ColorDesc,
			"ColorCode": self.ColorCode,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Size(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_size"
	SizeId = db.Column("SizeId",db.Integer,nullable=False,primary_key=True)
	SizeName = db.Column("SizeName",db.String(100),nullable=False)
	SizeDesc = db.Column("SizeDesc",db.String(500))
	SizeTypeId = db.Column("SizeTypeId",db.Integer,db.ForeignKey("tbl_dk_size_type.SizeTypeId"))
	Res_size = db.relationship("Res_size",backref='size',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"sizeId": self.SizeId,
			"sizeName": self.SizeName,
			"sizeDesc": self.SizeDesc,
			"sizeTypeId": self.SizeTypeId
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"SizeName": self.SizeName,
			"SizeDesc": self.SizeDesc,
			"SizeTypeId": self.SizeTypeId,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Size_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_size_type"
	SizeTypeId = db.Column("SizeTypeId",db.Integer,nullable=False,primary_key=True)
	SizeTypeName = db.Column("SizeTypeName",db.String(100),nullable=False)
	SizeTypeDesc = db.Column("SizeTypeDesc",db.String(500))
	Size = db.relationship("Size",backref='size_type',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"sizeTypeId": self.SizeTypeId,
			"sizeTypeName": self.SizeTypeName,
			"sizeTypeDesc": self.SizeTypeDesc
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"SizeTypeName": self.SizeTypeName,
			"SizeTypeDesc": self.SizeTypeDesc,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Unit(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_unit"
	UnitId = db.Column("UnitId",db.Integer,nullable=False,primary_key=True)
	UnitName_tkTM = db.Column("UnitName_tkTM",db.String(100))
	UnitDesc_tkTM = db.Column("UnitDesc_tkTM",db.String(100))
	UnitName_ruRU = db.Column("UnitName_ruRU",db.String(100))
	UnitDesc_ruRU = db.Column("UnitDesc_ruRU",db.String(100))
	UnitName_enUS = db.Column("UnitName_enUS",db.String(100))
	UnitDesc_enUS = db.Column("UnitDesc_enUS",db.String(100))
	Res_unit = db.relationship("Res_unit",backref='unit',lazy=True)
	Barcode = db.relationship("Barcode",backref='unit',lazy=True)
	Resource = db.relationship("Resource",backref='unit',lazy=True)
	Inv_line = db.relationship("Inv_line",backref='unit',lazy=True)
	Order_inv_line = db.relationship("Order_inv_line",backref='unit',lazy=True)
	Res_price = db.relationship("Res_price",backref='unit',lazy=True)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='unit',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='unit',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='unit',lazy=True)
	Production_line = db.relationship("Production_line",backref='unit',lazy=True)

	def to_json_api(self):
		json_data = {
			"UnitName_tkTM": self.UnitName_tkTM,
			"UnitDesc_tkTM": self.UnitDesc_tkTM,
			"UnitName_ruRU": self.UnitName_ruRU,
			"UnitDesc_ruRU": self.UnitDesc_ruRU,
			"UnitName_enUS": self.UnitName_enUS,
			"UnitDesc_enUS": self.UnitDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Usage_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_usage_status"
	UsageStatusId = db.Column("UsageStatusId",db.Integer,nullable=False,primary_key=True)
	UsageStatusName_tkTM = db.Column("UsageStatusName_tkTM",db.String(100))
	UsageStatusDesc_tkTM = db.Column("UsageStatusDesc_tkTM",db.String(500))
	UsageStatusName_ruRU = db.Column("UsageStatusName_ruRU",db.String(100))
	UsageStatusDesc_ruRU = db.Column("UsageStatusDesc_ruRU",db.String(500))
	UsageStatusName_enUS = db.Column("UsageStatusName_enUS",db.String(100))
	UsageStatusDesc_enUS = db.Column("UsageStatusDesc_enUS",db.String(500))
	Resource = db.relationship("Resource",backref='usage_status',lazy=True)
	Res_price_group = db.relationship("Res_price_group",backref='usage_status',lazy=True)
	Res_price_rule = db.relationship("Res_price_rule",backref='usage_status',lazy=True)

	def to_json_api(self):
		json_data = {
			"UsageStatusName_tkTM": self.UsageStatusName_tkTM,
			"UsageStatusDesc_tkTM": self.UsageStatusDesc_tkTM,
			"UsageStatusName_ruRU": self.UsageStatusName_ruRU,
			"UsageStatusDesc_ruRU": self.UsageStatusDesc_ruRU,
			"UsageStatusName_enUS": self.UsageStatusName_enUS,
			"UsageStatusDesc_enUS": self.UsageStatusDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Discount_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_discount_type"
	DiscTypeId = db.Column("DiscTypeId",db.Integer,nullable=False,primary_key=True)
	DiscTypeName_tkTM = db.Column("DiscTypeName_tkTM",db.String(100),nullable=False)
	DiscTypeDesc_tkTM = db.Column("DiscTypeDesc_tkTM",db.String(500))
	DiscTypeName_ruRU = db.Column("DiscTypeName_ruRU",db.String(100))
	DiscTypeDesc_ruRU = db.Column("DiscTypeDesc_ruRU",db.String(500))
	DiscTypeName_enUS = db.Column("DiscTypeName_enUS",db.String(100))
	DiscTypeDesc = db.Column("DiscTypeDesc",db.String(500))
	Res_discount = db.relationship("Res_discount",backref='discount_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"DiscTypeId": self.DiscTypeId,
			"DiscTypeName_tkTM": self.DiscTypeName_tkTM,
			"DiscTypeDesc_tkTM": self.DiscTypeDesc_tkTM,
			"DiscTypeName_ruRU": self.DiscTypeName_ruRU,
			"DiscTypeDesc_ruRU": self.DiscTypeDesc_ruRU,
			"DiscTypeName_enUS": self.DiscTypeName_enUS,
			"DiscTypeDesc": self.DiscTypeDesc,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Exc_rate(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_exc_rate"
	ExcRateId = db.Column("ExcRateId",db.Integer,nullable=False,primary_key=True)
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ExcRateDate = db.Column("ExcRateDate",db.DateTime)
	ExcRateInValue = db.Column("ExcRateInValue",db.Float,default=0.0)
	ExcRateOutValue = db.Column("ExcRateOutValue",db.Float,default=0.0)
	
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ExcRateId": self.ExcRateId,
			"CurrencyId": self.CurrencyId,
			"ExcRateDate": apiDataFormat(self.ExcRateDate),
			"ExcRateInValue": self.ExcRateInValue,
			"ExcRateOutValue": self.ExcRateOutValue,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Inv_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_line"
	InvLineId = db.Column("InvLineId",db.Integer,nullable=False,primary_key=True)
	InvLineGuid = db.Column("InvLineGuid",UUID(as_uuid=True),unique=True)
	InvId = db.Column("InvId",db.Integer,db.ForeignKey("tbl_dk_invoice.InvId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column("LastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	InvLineRegNo = db.Column("InvLineRegNo",db.String(100),nullable=False,unique=True)
	InvLineDesc = db.Column("InvLineDesc",db.String(500))
	InvLineAmount = db.Column("InvLineAmount",db.Float)
	InvLinePrice = db.Column("InvLinePrice",db.Float,default=0.0)
	InvLineTotal = db.Column("InvLineTotal",db.Float,default=0.0)
	InvLineExpenseAmount = db.Column("InvLineExpenseAmount",db.Float,default=0.0)
	InvLineTaxAmount = db.Column("InvLineTaxAmount",db.Float,default=0.0)
	InvLineDiscAmount = db.Column("InvLineDiscAmount",db.Float,default=0.0)
	InvLineFTotal = db.Column("InvLineFTotal",db.Float,default=0.0)
	InvLineDate = db.Column("InvLineDate",db.DateTime,default=datetime.now)
	ExcRateValue = db.Column("ExcRateValue",db.Float,default=0.0)
	Inv_line_det = db.relationship("Inv_line_det",backref='inv_line',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='inv_line',lazy=True)
	# Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='inv_line',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		inv_line = {
			"InvLineId": self.InvLineId,
			"InvLineGuid": self.InvLineGuid,
			"InvId": self.InvId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"LastVendorId": self.LastVendorId,
			"InvLineDesc": self.InvLineDesc,
			"InvLineAmount": self.InvLineAmount,
			"InvLinePrice": self.InvLinePrice,
			"InvLineTotal": self.InvLineTotal,
			"InvLineExpenseAmount": self.InvLineExpenseAmount,
			"InvLineTaxAmount": self.InvLineTaxAmount,
			"InvLineDiscAmount": self.InvLineDiscAmount,
			"InvLineFTotal": self.InvLineFTotal,
			"InvLineDate": self.InvLineDate,
			"ExcRateValue": self.ExcRateValue,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_line


class Inv_line_det(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_line_det"
	InvLineDetId = db.Column("InvLineDetId",db.Integer,nullable=False,primary_key=True)
	InvLineId = db.Column("InvLineId",db.Integer,db.ForeignKey("tbl_dk_inv_line.InvLineId"))
	InvLineDetTypeId = db.Column("InvLineDetTypeId",db.Integer,db.ForeignKey("tbl_dk_inv_line_det_type.InvLineDetTypeId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	InvLineDetResSN = db.Column("InvLineDetResSN",db.String(100))
	InvLineDetSLStartDate = db.Column("InvLineDetSLStartDate",db.DateTime)
	InvLineDetSLEndDate = db.Column("InvLineDetSLEndDate",db.DateTime)
	InvLineDetAmount = db.Column("InvLineDetAmount",db.Float)
	InvLineDetAmountBalance = db.Column("InvLineDetAmountBalance",db.Float)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		inv_line_det = {
			"InvLineDetId": self.InvLineDetId,
			"InvLineId": self.InvLineId,
			"InvLineDetTypeId": self.InvLineDetTypeId,
			"ResId": self.ResId,
			"InvLineDetResSN": self.InvLineDetResSN,
			"InvLineDetSLStartDate": self.InvLineDetSLStartDate,
			"InvLineDetSLEndDate": self.InvLineDetSLEndDate,
			"InvLineDetAmount": self.InvLineDetAmount,
			"InvLineDetAmountBalance": self.InvLineDetAmountBalance,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_line_det


class Inv_line_det_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_line_det_type"
	InvLineDetTypeId = db.Column("InvLineDetTypeId",db.Integer,nullable=False,primary_key=True)
	InvLineDetTypeName_tkTM = db.Column("InvLineDetTypeName_tkTM",db.String(100),nullable=False)
	InvLineDetTypeDesc_tkTM = db.Column("InvLineDetTypeDesc_tkTM",db.String(500))
	InvLineDetTypeName_ruRU = db.Column("InvLineDetTypeName_ruRU",db.String(100))
	InvLineDetTypeDesc_ruRU = db.Column("InvLineDetTypeDesc_ruRU",db.String(500))
	InvLineDetTypeName_enUS = db.Column("InvLineDetTypeName_enUS",db.String(100))
	InvLineDetTypeDesc_enUS = db.Column("InvLineDetTypeDesc_enUS",db.String(500))
	Inv_line_det = db.relationship("Inv_line_det",backref='inv_line_det_type',lazy=True)

	def to_json_api(self):
		inv_line_det_type = {
			"InvLineDetTypeId": self.InvLineDetTypeId,
			"InvLineDetTypeName_tkTM": self.InvLineDetTypeName_tkTM,
			"InvLineDetTypeDesc_tkTM": self.InvLineDetTypeDesc_tkTM,
			"InvLineDetTypeName_ruRU": self.InvLineDetTypeName_ruRU,
			"InvLineDetTypeDesc_ruRU": self.InvLineDetTypeDesc_ruRU,
			"InvLineDetTypeName_enUS": self.InvLineDetTypeName_enUS,
			"InvLineDetTypeDesc_enUS": self.InvLineDetTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_line_det_type


class Inv_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_status"
	InvStatId = db.Column("InvStatId",db.Integer,nullable=False,primary_key=True)
	InvStatName_tkTM = db.Column("InvStatName_tkTM",db.String(100),nullable=False)
	InvStatDesc_tkTM = db.Column("InvStatDesc_tkTM",db.String(500))
	InvStatName_ruRU = db.Column("InvStatName_ruRU",db.String(100))
	InvStatDesc_ruRU = db.Column("InvStatDesc_ruRU",db.String(500))
	InvStatName_enUS = db.Column("InvStatName_enUS",db.String(100))
	InvStatDesc_enUS = db.Column("InvStatDesc_enUS",db.String(500))
	Order_inv = db.relationship("Order_inv",backref='inv_status',lazy=True)
	Invoice = db.relationship("Invoice",backref='inv_status',lazy=True)

	def to_json_api(self):
		inv_status = {
			"InvStatId": self.InvStatId,
			"InvStatName_tkTM": self.InvStatName_tkTM,
			"InvStatDesc_tkTM": self.InvStatDesc_tkTM,
			"InvStatName_ruRU": self.InvStatName_ruRU,
			"InvStatDesc_ruRU": self.InvStatDesc_ruRU,
			"InvStatName_enUS": self.InvStatName_enUS,
			"InvStatDesc_enUS": self.InvStatDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_status


class Inv_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_inv_type"
	InvTypeId = db.Column("InvTypeId",db.Integer,nullable=False,primary_key=True)
	InvTypeName_tkTM = db.Column("InvTypeName_tkTM",db.String(100),nullable=False)
	InvTypeDesc_tkTM = db.Column("InvTypeDesc_tkTM",db.String(500))
	InvTypeName_ruRU = db.Column("InvTypeName_ruRU",db.String(100))
	InvTypeDesc_ruRU = db.Column("InvTypeDesc_ruRU",db.String(500))
	InvTypeName_enUS = db.Column("InvTypeName_enUS",db.String(100))
	InvTypeDesc_enUS = db.Column("InvTypeDesc_enUS",db.String(500))
	Invoice = db.relationship("Invoice",backref='inv_type',lazy=True)

	def to_json_api(self):
		inv_type = {
			"InvTypeId": self.InvTypeId,
			"InvTypeName_tkTM": self.InvTypeName_tkTM,
			"InvTypeDesc_tkTM": self.InvTypeDesc_tkTM,
			"InvTypeName_ruRU": self.InvTypeName_ruRU,
			"InvTypeDesc_ruRU": self.InvTypeDesc_ruRU,
			"InvTypeName_enUS": self.InvTypeName_enUS,
			"InvTypeDesc_enUS": self.InvTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return inv_type


class Invoice(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_invoice"
	InvId = db.Column("InvId",db.Integer,nullable=False,primary_key=True)
	InvGuid = db.Column("InvGuid",UUID(as_uuid=True),unique=True)
	InvTypeId = db.Column("InvTypeId",db.Integer,db.ForeignKey("tbl_dk_inv_type.InvTypeId"))
	InvStatId = db.Column("InvStatId",db.Integer,db.ForeignKey("tbl_dk_inv_status.InvStatId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	PtId = db.Column("PtId",db.Integer,db.ForeignKey("tbl_dk_payment_type.PtId"))
	PmId = db.Column("PmId",db.Integer,db.ForeignKey("tbl_dk_payment_method.PmId"))
	InvLatitude = db.Column("InvLatitude",db.Float,default=0.0)
	InvLongitude = db.Column("InvLongitude",db.Float,default=0.0)
	InvRegNo = db.Column("InvRegNo",db.String(100),nullable=False,unique=True)
	InvDesc = db.Column("InvDesc",db.String(500))
	InvDate = db.Column("InvDate",db.DateTime,default=datetime.now)
	InvTotal = db.Column("InvTotal",db.Float)
	InvExpenseAmount = db.Column("InvExpenseAmount",db.Float,default=0.0)
	InvTaxAmount = db.Column("InvTaxAmount",db.Float,default=0.0)
	InvDiscountAmount = db.Column("InvDiscountAmount",db.Float,default=0.0)
	InvFTotal = db.Column("InvFTotal",db.Float,default=0.0)
	InvFTotalInWrite = db.Column("InvFTotalInWrite",db.String(100),default=0)
	InvModifyCount = db.Column("InvModifyCount",db.Integer,default=0)
	InvPrintCount = db.Column("InvPrintCount",db.Integer,default=0)
	InvCreditDays = db.Column("InvCreditDays",db.Integer,default=0)
	InvCreditDesc = db.Column("InvCreditDesc",db.String(100))
	Inv_line = db.relationship("Inv_line",backref='invoice',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='invoice',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		invoice = {
			"InvId": self.InvId,
			"InvGuid": self.InvGuid,
			"InvTypeId": self.InvTypeId,
			"InvStatId": self.InvStatId,
			"CurrencyId": self.CurrencyId,
			"RpAccId": self.RpAccId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhId": self.WhId,
			"WpId": self.WpId,
			"EmpId": self.EmpId,
			"PtId": self.PtId,
			"PmId": self.PmId,
			"InvLatitude": self.InvLatitude,
			"InvLongitude": self.InvLongitude,
			"InvRegNo": self.InvRegNo,
			"InvDesc": self.InvDesc,
			"InvDate": apiDataFormat(self.InvDate),
			"InvTotal": configureFloat(self.InvTotal),
			"InvExpenseAmount": configureFloat(self.InvExpenseAmount),
			"InvTaxAmount": configureFloat(self.InvTaxAmount),
			"InvDiscountAmount": configureFloat(self.InvDiscountAmount),
			"InvFTotal": configureFloat(self.InvFTotal),
			"InvFTotalInWrite": self.InvFTotalInWrite,
			"InvModifyCount": self.InvModifyCount,
			"InvPrintCount": self.InvPrintCount,
			"InvCreditDays": self.InvCreditDays,
			"InvCreditDesc": self.InvCreditDesc,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return invoice


class Order_inv(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_order_inv"
	OInvId = db.Column("OInvId",db.Integer,nullable=False,primary_key=True)
	OInvGuid = db.Column("OInvGuid",UUID(as_uuid=True),unique=True)
	OInvTypeId = db.Column("OInvTypeId",db.Integer,db.ForeignKey("tbl_dk_order_inv_type.OInvTypeId"))
	InvStatId = db.Column("InvStatId",db.Integer,db.ForeignKey("tbl_dk_inv_status.InvStatId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	PtId = db.Column("PtId",db.Integer,db.ForeignKey("tbl_dk_payment_type.PtId"))
	PmId = db.Column("PmId",db.Integer,db.ForeignKey("tbl_dk_payment_method.PmId"))
	PaymStatusId = db.Column("PaymStatusId",db.Integer,db.ForeignKey("tbl_dk_payment_status.PaymStatusId"))
	PaymCode = db.Column("PaymCode",db.String(500))
	PaymDesc = db.Column("PaymDesc",db.String(500))
	OInvLatitude = db.Column("OInvLatitude",db.Float,default=0.0)
	OInvLongitude = db.Column("OInvLongitude",db.Float,default=0.0)
	OInvRegNo = db.Column("OInvRegNo",db.String(100),nullable=False,unique=True)
	OInvDesc = db.Column("OInvDesc",db.String(500))
	OInvDate = db.Column("OInvDate",db.DateTime,default=datetime.now)
	OInvTotal = db.Column("OInvTotal",db.Float,default=0.0)
	OInvExpenseAmount = db.Column("OInvExpenseAmount",db.Float,default=0.0)
	OInvTaxAmount = db.Column("OInvTaxAmount",db.Float,default=0.0)
	OInvDiscountAmount = db.Column("OInvDiscountAmount",db.Float,default=0.0)
	OInvPaymAmount = db.Column("OInvPaymAmount",db.Float,default=0.0)
	OInvFTotal = db.Column("OInvFTotal",db.Float,default=0.0)
	OInvFTotalInWrite = db.Column("OInvFTotalInWrite",db.String(100))
	OInvModifyCount = db.Column("OInvModifyCount",db.Integer,default=0)
	OInvPrintCount = db.Column("OInvPrintCount",db.Integer,default=0)
	OInvCreditDays = db.Column("OInvCreditDays",db.Integer,default=0)
	OInvCreditDesc = db.Column("OInvCreditDesc",db.String(100))
	Order_inv_line = db.relationship("Order_inv_line",backref='order_inv',lazy='joined')

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		order_inv = {
			"OInvId": self.OInvId,
			"OInvGuid": self.OInvGuid,
			"OInvTypeId": self.OInvTypeId,
			"InvStatId": self.InvStatId,
			"CurrencyId": self.CurrencyId,
			"RpAccId": self.RpAccId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhId": self.WhId,
			"WpId": self.WpId,
			"EmpId": self.EmpId,
			"PtId": self.PtId,
			"PmId": self.PmId,
			"PaymStatusId": self.PaymStatusId,
			"PaymCode": self.PaymCode,
			"PaymDesc": self.PaymDesc,
			"OInvLatitude": self.OInvLatitude,
			"OInvLongitude": self.OInvLongitude,
			"OInvRegNo": self.OInvRegNo,
			"OInvDesc": self.OInvDesc,
			"OInvDate": apiDataFormat(self.OInvDate),
			"OInvTotal": configureFloat(self.OInvTotal),
			"OInvExpenseAmount": configureFloat(self.OInvExpenseAmount),
			"OInvTaxAmount": configureFloat(self.OInvTaxAmount),
			"OInvDiscountAmount": configureFloat(self.OInvDiscountAmount),
			"OInvPaymAmount": configureFloat(self.OInvPaymAmount),
			"OInvFTotal": configureFloat(self.OInvFTotal),
			"OInvFTotalInWrite": self.OInvFTotalInWrite,
			"OInvModifyCount": self.OInvModifyCount,
			"OInvPrintCount": self.OInvPrintCount,
			"OInvCreditDays": self.OInvCreditDays,
			"OInvCreditDesc": self.OInvCreditDesc,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return order_inv


class Order_inv_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_order_inv_line"
	OInvLineId = db.Column("OInvLineId",db.Integer,nullable=False,primary_key=True)
	OInvLineGuid = db.Column("OInvLineGuid",UUID(as_uuid=True),unique=True)
	OInvId = db.Column("OInvId",db.Integer,db.ForeignKey("tbl_dk_order_inv.OInvId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column("LastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	OInvLineRegNo = db.Column("OInvLineRegNo",db.String(100),nullable=False,unique=True)
	OInvLineDesc = db.Column("OInvLineDesc",db.String(500))
	OInvLineAmount = db.Column("OInvLineAmount",db.Float,default=0.0)
	OInvLinePrice = db.Column("OInvLinePrice",db.Float,default=0.0)
	OInvLineTotal = db.Column("OInvLineTotal",db.Float,default=0.0)
	OInvLineExpenseAmount = db.Column("OInvLineExpenseAmount",db.Float,default=0.0)
	OInvLineTaxAmount = db.Column("OInvLineTaxAmount",db.Float,default=0.0)
	OInvLineDiscAmount = db.Column("OInvLineDiscAmount",db.Float,default=0.0)
	OInvLineFTotal = db.Column("OInvLineFTotal",db.Float,default=0.0)
	OInvLineDate = db.Column("OInvLineDate",db.DateTime,default=datetime.now)
	ExcRateValue = db.Column("ExcRateValue",db.Float,default=0.0)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		order_inv_line = {
			"OInvLineId": self.OInvLineId,
			"OInvLineGuid": self.OInvLineGuid,
			"OInvId": self.OInvId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"LastVendorId": self.LastVendorId,
			"OInvLineRegNo": self.OInvLineRegNo,
			"OInvLineDesc": self.OInvLineDesc,
			"OInvLineAmount": configureFloat(self.OInvLineAmount),
			"OInvLinePrice": configureFloat(self.OInvLinePrice),
			"OInvLineTotal": configureFloat(self.OInvLineTotal),
			"OInvLineExpenseAmount": configureFloat(self.OInvLineExpenseAmount),
			"OInvLineTaxAmount": configureFloat(self.OInvLineTaxAmount),
			"OInvLineDiscAmount": configureFloat(self.OInvLineDiscAmount),
			"OInvLineFTotal": configureFloat(self.OInvLineFTotal),
			"OInvLineDate": apiDataFormat(self.OInvLineDate),
			"ExcRateValue": self.ExcRateValue,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return order_inv_line


class Order_inv_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_order_inv_type"
	OInvTypeId = db.Column("OInvTypeId",db.Integer,nullable=False,primary_key=True)
	OInvTypeName_tkTM = db.Column("OInvTypeName_tkTM",db.String(100),nullable=False)
	OInvTypeDesc_tkTM = db.Column("OInvTypeDesc_tkTM",db.String(500))
	OInvTypeName_ruRU = db.Column("OInvTypeName_ruRU",db.String(100))
	OInvTypeDesc_ruRU = db.Column("OInvTypeDesc_ruRU",db.String(500))
	OInvTypeName_enUS = db.Column("OInvTypeName_enUS",db.String(100))
	OInvTypeDesc_enUS = db.Column("OInvTypeDesc_enUS",db.String(500))
	Order_inv = db.relationship("Order_inv",backref='order_inv_type',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"OInvTypeId": self.OInvTypeId,
			"OInvTypeName_tkTM": self.OInvTypeName_tkTM,
			"OInvTypeDesc_tkTM": self.OInvTypeDesc_tkTM,
			"OInvTypeName_ruRU": self.OInvTypeName_ruRU,
			"OInvTypeDesc_ruRU": self.OInvTypeDesc_ruRU,
			"OInvTypeName_enUS": self.OInvTypeName_enUS,
			"OInvTypeDesc_enUS": self.OInvTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Payment_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_payment_status"
	PaymStatusId = db.Column("PaymStatusId",db.Integer,nullable=False,primary_key=True)
	PaymStatusName_tkTM = db.Column("PaymStatusName_tkTM",db.String(100))
	PaymStatusDesc_tkTM = db.Column("PaymStatusDesc_tkTM",db.String(500))
	PaymStatusName_ruRU = db.Column("PaymStatusName_ruRU",db.String(100))
	PaymStatusDesc_ruRU = db.Column("PaymStatusDesc_ruRU",db.String(500))
	PaymStatusName_enUS = db.Column("PaymStatusName_enUS",db.String(100))
	PaymStatusDesc_enUS = db.Column("PaymStatusDesc_enUS",db.String(500))
	Order_inv = db.relationship("Order_inv",backref='payment_status',lazy=True)

	def to_json_api(self):
		json_data = {
			"PaymStatusName_tkTM": self.PaymStatusName_tkTM,			
			"PaymStatusDesc_tkTM": self.PaymStatusDesc_tkTM,
			"PaymStatusName_ruRU": self.PaymStatusName_ruRU,
			"PaymStatusDesc_ruRU": self.PaymStatusDesc_ruRU,
			"PaymStatusName_enUS": self.PaymStatusName_enUS,
			"PaymStatusDesc_enUS": self.PaymStatusDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Payment_method(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_payment_method"
	PmId = db.Column("PmId",db.Integer,nullable=False,primary_key=True)	
	PmName = db.Column("PmName",db.String(100),nullable=False)
	PmDesc = db.Column("PmDesc",db.String(500))
	PmVisibleIndex = db.Column("PmVisibleIndex",db.Integer,default=0)
	Order_inv = db.relationship("Order_inv",backref='payment_method',lazy=True)
	Invoice = db.relationship("Invoice",backref='payment_method',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		payment_method = {
			"PmId": self.PmId,			
			"PmName": self.PmName,
			"PmDesc": self.PmDesc,
			"PmVisibleIndex": self.PmVisibleIndex,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return payment_method


class Payment_type(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_payment_type"
	PtId = db.Column("PtId",db.Integer,nullable=False,primary_key=True)
	PtName = db.Column("PtName",db.String(100),nullable=False)
	PtDesc = db.Column("PtDesc",db.String(500))
	PtVisibleIndex = db.Column("PtVisibleIndex",db.Integer,default=0)
	Order_inv = db.relationship("Order_inv",backref='payment_type',lazy=True)
	Invoice = db.relationship("Invoice",backref='payment_type',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		payment_type = {
			"PtId": self.PtId,
			"PtName": self.PtName,
			"PtDesc": self.PtDesc,
			"PtVisibleIndex": self.PtVisibleIndex,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return payment_type


class Representative(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_representative"
	ReprId = db.Column("ReprId",db.Integer,nullable=False,primary_key=True)
	ReprStatusId = db.Column("ReprStatusId",db.Integer,nullable=False,default=1)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	ReprRegNo = db.Column("ReprRegNo",db.String(100),nullable=False)
	ReprName = db.Column("ReprName",db.String(100),nullable=False)
	ReprDesc = db.Column("ReprDesc",db.String(500))
	ReprProfession = db.Column("ReprProfession",db.String(100))
	ReprMobilePhoneNumber = db.Column("ReprMobilePhoneNumber",db.String(100))
	ReprHomePhoneNumber = db.Column("ReprHomePhoneNumber",db.String(100))
	ReprWorkPhoneNumber = db.Column("ReprWorkPhoneNumber",db.String(100))
	ReprWorkFaxNumber = db.Column("ReprWorkFaxNumber",db.String(100))
	ReprZipCode = db.Column("ReprZipCode",db.String(100))
	ReprEMail = db.Column("ReprEMail",db.String(100))
	CreatedDate = db.Column("CreatedDate",db.DateTime,default=datetime.now)
	ModifiedDate = db.Column("ModifiedDate",db.DateTime,default=datetime.now)
	CreatedUId = db.Column("CreatedUId",db.Integer,default=0)
	ModifiedUId = db.Column("ModifiedUId",db.Integer,default=0)
	MyProperty = db.Column("MyProperty",db.Integer)
	Rp_acc = db.relationship("Rp_acc",backref='representative',foreign_keys='Rp_acc.ReprId',lazy='joined')

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ReprId": self.ReprId,
			"ReprStatusId": self.ReprStatusId,
			"CId": self.CId,
			"DivId": self.DivId,
			"RpAccId": self.RpAccId,
			"GenderId": self.GenderId,
			"ReprRegNo": self.ReprRegNo,
			"ReprName": self.ReprName,
			"ReprDesc": self.ReprDesc,
			"ReprProfession": self.ReprProfession,
			"ReprMobilePhoneNumber": self.ReprMobilePhoneNumber,
			"ReprHomePhoneNumber": self.ReprHomePhoneNumber,
			"ReprWorkPhoneNumber": self.ReprWorkPhoneNumber,
			"ReprWorkFaxNumber": self.ReprWorkFaxNumber,
			"ReprZipCode": self.ReprZipCode,
			"ReprEMail": self.ReprEMail,
			"CreatedDate": self.CreatedDate,
			"ModifiedDate": self.ModifiedDate,
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"MyProperty": self.MyProperty,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Resource(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_resource"
	ResId = db.Column("ResId",db.Integer,nullable=False,primary_key=True)
	ResGuid = db.Column("ResGuid",UUID(as_uuid=True),unique=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResCatId = db.Column("ResCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BrandId = db.Column("BrandId",db.Integer,db.ForeignKey("tbl_dk_brand.BrandId"))
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	ResTypeId = db.Column("ResTypeId",db.Integer,db.ForeignKey("tbl_dk_res_type.ResTypeId"))
	ResMainImgId = db.Column("ResMainImgId",db.Integer,default=0)
	ResMakerId = db.Column("ResMakerId",db.Integer,db.ForeignKey("tbl_dk_res_maker.ResMakerId"))
	ResLastVendorId = db.Column("ResLastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResRegNo = db.Column("ResRegNo",db.String(50),nullable=False,unique=True)
	ResName = db.Column("ResName",db.String(255),nullable=False)
	ResDesc = db.Column("ResDesc",db.String(500))
	ResFullDesc = db.Column("ResFullDesc",db.String(1500))
	ResWidth = db.Column("ResWidth",db.Float,default=0.0)
	ResHeight = db.Column("ResHeight",db.Float,default=0.0)
	ResLength = db.Column("ResLength",db.Float,default=0.0)
	ResWeight = db.Column("ResWeight",db.Float,default=0.0)
	ResProductionOnSale = db.Column("ResProductionOnSale",db.Boolean,default=False)
	ResMinSaleAmount = db.Column("ResMinSaleAmount",db.Float,default=0.0)
	ResMaxSaleAmount = db.Column("ResMaxSaleAmount",db.Float,default=0.0)
	ResMinSalePrice = db.Column("ResMinSalePrice",db.Float,default=0.0)
	ResMaxSalePrice = db.Column("ResMaxSalePrice",db.Float,default=0.0)
	Image = db.relationship("Image",backref='resource',lazy=True)
	Barcode = db.relationship("Barcode",backref='resource',lazy=True)
	Res_color = db.relationship("Res_color",backref='resource',lazy=True)
	Res_size = db.relationship("Res_size",backref='resource',lazy=True)
	Res_translations = db.relationship("Res_translations",backref='resource',lazy=True)
	Res_unit = db.relationship("Res_unit",backref='resource',lazy=True)
	# sales and purchases
	Inv_line = db.relationship("Inv_line",backref='resource',lazy=True)
	Inv_line_det = db.relationship("Inv_line_det",backref='resource',lazy=True)	
	Order_inv_line = db.relationship("Order_inv_line",backref='resource',lazy=True)
	Res_price = db.relationship("Res_price",backref='resource',lazy=True)
	# quantity of a resource
	Res_total = db.relationship("Res_total",backref='resource',lazy=True)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='resource',lazy=True)
	Res_transaction = db.relationship("Res_transaction",backref='resource',lazy=True)
	Rp_acc_resource = db.relationship("Rp_acc_resource",backref='resource',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='resource',lazy=True)
	Res_price_rule = db.relationship("Res_price_rule",backref='resource',lazy=True)
	Res_discount = db.relationship("Res_discount",foreign_keys='Res_discount.SaleResId',backref='resource',lazy=True)
	Res_discount = db.relationship("Res_discount",foreign_keys='Res_discount.GiftResId',backref='resource',lazy=True)
	
	Wish = db.relationship("Wish",backref='resource',lazy=True)
	Production = db.relationship("Production",backref='resource',lazy=True)
	Production_line = db.relationship("Production_line",backref='resource',lazy=True)
	Rating = db.relationship("Rating",backref='resource',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	
	def to_json_api(self):
		json_data = {
			"resId": self.ResId,
			"companyId": self.CId,
			"divisionId": self.DivId,
			"resourceCategoryId": self.ResCatId,
			"unitId": self.UnitId,
			"brandId": self.BrandId,
			"usageStatusId": self.UsageStatusId,
			"resTypeId": self.ResTypeId,
			"mainImageId": self.ResMainImgId,
			"resMakerId": self.ResMakerId,
			"lastVendorId": self.ResLastVendorId,
			"regNo": self.ResRegNo,
			"resourceName": self.ResName,
			"resourceDesc": self.ResDesc,
			"resourceFullDesc": self.ResFullDesc,
			"resourceWidth": self.ResWidth,
			"resourceHeight": self.ResHeight,
			"resourceLength": self.ResLength,
			"resourceWeight": self.ResWeight,
			"resourceOnSale": self.ResProductionOnSale,
			"resourceMinSaleAmount": self.ResMinSaleAmount,
			"resourceMaxSaleAmount": self.ResMaxSaleAmount,
			"resourceMinSalePrice": self.ResMinSalePrice,
			"resourceMaxSalePrice": self.ResMaxSalePrice
		}
		return json_data

	def to_json_api(self):
		data = {
			"ResId": self.ResId,
			"ResGuid": self.ResGuid,
			"CId": self.CId,
			"DivId": self.DivId,
			"ResCatId": self.ResCatId,
			"UnitId": self.UnitId,
			"BrandId": self.BrandId,
			"UsageStatusId": self.UsageStatusId,
			"ResTypeId": self.ResTypeId,
			"ResMainImgId": self.ResMainImgId,
			"ResMakerId": self.ResMakerId,
			"ResLastVendorId": self.ResLastVendorId,
			"ResRegNo": self.ResRegNo,
			"ResName": self.ResName,
			"ResDesc": self.ResDesc,
			"ResFullDesc": self.ResFullDesc,
			"ResWidth": configureFloat(self.ResWidth),
			"ResHeight": configureFloat(self.ResHeight),
			"ResLength": configureFloat(self.ResLength),
			"ResWeight": configureFloat(self.ResWeight),
			"ResProductionOnSale": self.ResProductionOnSale,
			"ResMinSaleAmount": configureFloat(self.ResMinSaleAmount),
			"ResMaxSaleAmount": configureFloat(self.ResMaxSaleAmount),
			"ResMinSalePrice": configureFloat(self.ResMinSalePrice),
			"ResMaxSalePrice": configureFloat(self.ResMaxSalePrice),
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return data


class Res_category(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_category"
	ResCatId = db.Column("ResCatId",db.Integer,nullable=False,primary_key=True)
	ResOwnerCatId = db.Column("ResOwnerCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ResCatVisibleIndex = db.Column("ResCatVisibleIndex",db.Integer,default=0)
	IsMain = db.Column("IsMain",db.Boolean,default=False)
	ResCatName = db.Column("ResCatName",db.String(100),nullable=False)
	ResCatDesc = db.Column("ResCatDesc",db.String(500),default='')
	ResCatIconName = db.Column("ResCatIconName",db.String(100))
	ResCatIconFilePath = db.Column("ResCatIconFilePath",db.String(255))
	ResCatIconData = db.Column("ResCatIconData",db.String(100000))
	Resource = db.relationship("Resource",backref='res_category',lazy=True)
	Image = db.relationship("Image",backref='res_category',lazy=True)
	Translations = db.relationship("Translations",backref='res_category',lazy=True)
	Res_category = db.relationship("Res_category",remote_side=ResCatId,backref='subcategory',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ownerCategoryId": self.ResOwnerCatId,
			"visibleIndex": self.ResCatVisibleIndex,
			"isMain": self.IsMain,
			"categoryName": self.ResCatName,
			"categoryDesc": self.ResCatDesc,
			"categoryIcon": self.ResCatIconName
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"ResCatId": self.ResCatId,
			"ResOwnerCatId": self.ResOwnerCatId or 0,
			"ResCatVisibleIndex": self.ResCatVisibleIndex or 0,
			"IsMain": self.IsMain,
			"ResCatName": self.ResCatName,
			"ResCatDesc": self.ResCatDesc,
			"ResCatIconName": self.ResCatIconName,
			"ResCatIconFilePath": self.ResCatIconFilePath,
			"ResCatIconData": self.ResCatIconData,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_maker(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_maker"
	ResMakerId = db.Column("ResMakerId",db.Integer,nullable=False,primary_key=True)
	ResMakerName = db.Column("ResMakerName",db.String(100),nullable=False)
	ResMakerDesc = db.Column("ResMakerDesc",db.String(500))
	ResMakerSite = db.Column("ResMakerSite",db.String(150))
	ResMakerMail = db.Column("ResMakerMail",db.String(100))
	ResMakerPhone1 = db.Column("ResMakerPhone1",db.String(100))
	ResMakerPhone2 = db.Column("ResMakerPhone2",db.String(100))
	Resource = db.relationship("Resource",backref='res_maker',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResMakerId": self.ResMakerId,
			"ResMakerName": self.ResMakerName,
			"ResMakerDesc": self.ResMakerDesc,
			"ResMakerSite": self.ResMakerSite,
			"ResMakerMail": self.ResMakerMail,
			"ResMakerPhone1": self.ResMakerPhone1,
			"ResMakerPhone2": self.ResMakerPhone2,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_color"
	RcId = db.Column("RcId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ColorId = db.Column("ColorId",db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json_api(self):
		json_data = {
			"rcId": self.RcId,
			"resId": self.ResId,
			"colorId": self.ColorId
		}
		return json_data


class Res_size(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_size"
	RsId = db.Column("RsId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SizeId = db.Column("SizeId",db.Integer,db.ForeignKey("tbl_dk_size.SizeId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json_api(self):
		json_data = {
			"rsId": self.RsId,
			"resId": self.ResId,
			"sizeId": self.SizeId
		}
		return json_data


class Res_discount(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_discount"
	ResDiscId = db.Column("ResDiscId",db.Integer,nullable=False,primary_key=True)
	SaleCardId = db.Column("SaleCardId",db.Integer,db.ForeignKey("tbl_dk_sale_card.SaleCardId"))
	ResDiscRegNo = db.Column("ResDiscRegNo",db.String(100),nullable=False)
	SaleResId = db.Column("SaleResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SaleResAmount = db.Column("SaleResAmount",db.Float,default=0.0)
	DiscTypeId = db.Column("DiscTypeId",db.Integer,db.ForeignKey("tbl_dk_discount_type.DiscTypeId"))
	DiscValue = db.Column("DiscValue",db.Float,default=0.0)
	DiscDesc = db.Column("DiscDesc",db.String(500))
	ResDiscStartDate = db.Column("ResDiscStartDate",db.DateTime)
	ResDiscEndDate = db.Column("ResDiscEndDate",db.DateTime)
	ResDiscIsActive = db.Column("ResDiscIsActive",db.Boolean,default=True)
	GiftResId = db.Column("GiftResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	GiftResAmount = db.Column("GiftResAmount",db.Float,default=0.0)
	GiftResDiscValue = db.Column("GiftResDiscValue",db.Float,default=0.0)
	Sale_card = db.relationship("Sale_card",backref='res_discount',foreign_keys='Sale_card.ResDiscId',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResDiscId": self.ResDiscId,
			"SaleCardId": self.SaleCardId,
			"ResDiscRegNo": self.ResDiscRegNo,
			"SaleResId": self.SaleResId,
			"SaleResAmount": self.SaleResAmount,
			"DiscTypeId": self.DiscTypeId,
			"DiscValue": self.DiscValue,
			"DiscDesc": self.DiscDesc,
			"ResDiscStartDate": self.ResDiscStartDate,
			"ResDiscEndDate": self.ResDiscEndDate,
			"ResDiscIsActive": self.ResDiscIsActive,
			"GiftResId": self.GiftResId,
			"GiftResAmount": self.GiftResAmount,
			"GiftResDiscValue": self.GiftResDiscValue,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_price(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_price"
	ResPriceId = db.Column("ResPriceId",db.Integer,nullable=False,primary_key=True)
	ResPriceTypeId = db.Column("ResPriceTypeId",db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResPriceRegNo = db.Column("ResPriceRegNo",db.String(100),nullable=False)
	ResPriceValue = db.Column("ResPriceValue",db.Float,default=0.0)
	PriceStartDate = db.Column("PriceStartDate",db.DateTime)
	PriceEndDate = db.Column("PriceEndDate",db.DateTime)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"resPriceId": self.ResPriceId,
			"resPriceTypeId": self.ResPriceTypeId,
			"resPriceGroupId": self.ResPriceGroupId,
			"unitId": self.UnitId,
			"currencyId": self.CurrencyId,
			"resId": self.ResId,
			"resPriceRegNo": self.ResPriceRegNo,
			"resPriceValue": self.ResPriceValue,
			"priceStartDate": apiDataFormat(self.PriceStartDate),
			"priceEndDate": self.PriceEndDate
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"ResPriceId": self.ResPriceId,
			"ResPriceTypeId": self.ResPriceTypeId,
			"ResPriceGroupId": self.ResPriceGroupId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"ResPriceRegNo": self.ResPriceRegNo,
			"ResPriceValue": self.ResPriceValue,
			"PriceStartDate": apiDataFormat(self.PriceStartDate),
			"PriceEndDate": apiDataFormat(self.PriceEndDate),
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_price_group(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_price_group"
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,nullable=False,primary_key=True)
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	ResPriceGroupName = db.Column("ResPriceGroupName",db.String(100),nullable=False)
	ResPriceGroupDesc = db.Column("ResPriceGroupDesc",db.String(500))
	ResPriceGroupAMEnabled = db.Column("ResPriceGroupAMEnabled",db.Boolean,default=False)
	FromResPriceTypeId = db.Column("FromResPriceTypeId",db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ToResPriceTypeId = db.Column("ToResPriceTypeId",db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ResPriceGroupAMPerc = db.Column("ResPriceGroupAMPerc",db.Float,default=0.0)
	RoundingType = db.Column("RoundingType",db.Integer,default=1)
	Res_price = db.relationship("Res_price",backref='res_price_group',lazy=True)
	Sale_card = db.relationship("Sale_card",backref='res_price_group',lazy=True)
	Res_price_rule = db.relationship("Res_price_rule",backref='res_price_group',lazy=True)
	User = db.relationship("User",backref='res_price_group',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='res_price_group',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResPriceGroupId": self.ResPriceGroupId,
			"UsageStatusId": self.UsageStatusId,
			"ResPriceGroupName": self.ResPriceGroupName,
			"ResPriceGroupDesc": self.ResPriceGroupDesc,
			"ResPriceGroupAMEnabled": self.ResPriceGroupAMEnabled,
			"FromResPriceTypeId": self.FromResPriceTypeId,
			"ToResPriceTypeId": self.ToResPriceTypeId,
			"ResPriceGroupAMPerc": self.ResPriceGroupAMPerc,
			"RoundingType": self.RoundingType,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_price_type(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_price_type"
	ResPriceTypeId = db.Column("ResPriceTypeId",db.Integer,nullable=False,primary_key=True)
	ResPriceTypeName_tkTM = db.Column("ResPriceTypeName_tkTM",db.String(100),nullable=False)
	ResPriceTypeDesc_tkTM = db.Column("ResPriceTypeDesc_tkTM",db.String(500))
	ResPriceTypeName_ruRU = db.Column("ResPriceTypeName_ruRU",db.String(100))
	ResPriceTypeDesc_ruRU = db.Column("ResPriceTypeDesc_ruRU",db.String(500))
	ResPriceTypeName_enUS = db.Column("ResPriceTypeName_enUS",db.String(100))
	ResPriceTypeDesc_enUS = db.Column("ResPriceTypeDesc_enUS",db.String(500))
	Res_price = db.relationship("Res_price",backref='res_price_type',lazy=True)
	# multiple relationship
	Res_price_group = db.relationship("Res_price_group",foreign_keys='Res_price_group.FromResPriceTypeId',backref='res_price_type',lazy=True)
	Res_price_group = db.relationship("Res_price_group",foreign_keys='Res_price_group.ToResPriceTypeId',backref='res_price_type',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='res_price_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResPriceTypeId": self.ResPriceTypeId,
			"ResPriceTypeName_tkTM": self.ResPriceTypeName_tkTM,
			"ResPriceTypeDesc_tkTM": self.ResPriceTypeDesc_tkTM,
			"ResPriceTypeName_ruRU": self.ResPriceTypeName_ruRU,
			"ResPriceTypeDesc_ruRU": self.ResPriceTypeDesc_ruRU,
			"ResPriceTypeName_enUS": self.ResPriceTypeName_enUS,
			"ResPriceTypeDesc_enUS": self.ResPriceTypeDesc_enUS,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_price_rule(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_price_rule"
	RprId = db.Column("RprId",db.Integer,nullable=False,primary_key=True)
	UsageStatusId = db.Column("UsageStatusId",db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	ResMinAmount = db.Column("ResMinAmount",db.Float)
	ResMaxAmount = db.Column("ResMaxAmount",db.Float)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"RprId": self.RprId,
			"UsageStatusId": self.UsageStatusId,
			"ResId": self.ResId,
			"ResPriceGroupId": self.ResPriceGroupId,
			"ResMinAmount": self.ResMinAmount,
			"ResMaxAmount": self.ResMaxAmount,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_total(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_total"
	ResTotId = db.Column("ResTotId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	ResTotBalance = db.Column("ResTotBalance",db.Float,default=0.0)
	ResTotInAmount = db.Column("ResTotInAmount",db.Float,default=0.0)
	ResPendingTotalAmount = db.Column("ResPendingTotalAmount",db.Float,default=0.0)
	ResTotOutAmount = db.Column("ResTotOutAmount",db.Float,default=0.0)
	ResTotLastTrDate = db.Column("ResTotLastTrDate",db.DateTime,default=datetime.now)
	ResTotPurchAvgPrice = db.Column("ResTotPurchAvgPrice",db.Float,default=0.0)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResTotId": self.ResTotId,
			"ResId": self.ResId,
			"CurrencyId": self.CurrencyId,
			"WhId": self.WhId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WpId": self.WpId,
			"ResTotBalance": self.ResTotBalance,
			"ResTotInAmount": self.ResTotInAmount,
			"ResPendingTotalAmount": self.ResPendingTotalAmount,
			"ResTotOutAmount": self.ResTotOutAmount,
			"ResTotLastTrDate": apiDataFormat(self.ResTotLastTrDate),
			"ResTotPurchAvgPrice": self.ResTotPurchAvgPrice,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_trans_inv(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_trans_inv"
	ResTrInvId = db.Column("ResTrInvId",db.Integer,nullable=False,primary_key=True)
	ResTrInvTypeId = db.Column("ResTrInvTypeId",db.Integer,db.ForeignKey("tbl_dk_res_trans_inv_type.ResTrInvTypeId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhIdIn = db.Column("WhIdIn",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WhIdOut = db.Column("WhIdOut",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	ResTrInvRegNo = db.Column("ResTrInvRegNo",db.String(100),nullable=False)
	ResTrInvDesc = db.Column("ResTrInvDesc",db.String(500))
	ResTrInvDate = db.Column("ResTrInvDate",db.DateTime,default=datetime.now)
	ResTrInvTotal = db.Column("ResTrInvTotal",db.Float,default=0.0)
	ResTrInvExpAmount = db.Column("ResTrInvExpAmount",db.Float,default=0.0)
	ResTrInvTaxAmount = db.Column("ResTrInvTaxAmount",db.Float,default=0.0)
	ResTrInvFTotal = db.Column("ResTrInvFTotal",db.Float,default=0.0)
	ResTrInvFTotalInWrite = db.Column("ResTrInvFTotalInWrite",db.String(100))
	ResTrInvModifyCount = db.Column("ResTrInvModifyCount",db.Integer,default=0)
	ResTrInvPrintCount = db.Column("ResTrInvPrintCount",db.Integer,default=0)
	Res_trans_inv_line = db.relationship("Res_trans_inv_line",backref='res_trans_inv',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='res_trans_inv',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResTrInvId": self.ResTrInvId,
			"ResTrInvTypeId": self.ResTrInvTypeId,
			"CurrencyId": self.CurrencyId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhIdIn": self.WhIdIn,
			"WhIdOut": self.WhIdOut,
			"EmpId": self.EmpId,
			"ResTrInvRegNo": self.ResTrInvRegNo,
			"ResTrInvDesc": self.ResTrInvDesc,
			"ResTrInvDate": self.ResTrInvDate,
			"ResTrInvTotal": self.ResTrInvTotal,
			"ResTrInvExpAmount": self.ResTrInvExpAmount,
			"ResTrInvTaxAmount": self.ResTrInvTaxAmount,
			"ResTrInvFTotal": self.ResTrInvFTotal,
			"ResTrInvFTotalInWrite": self.ResTrInvFTotalInWrite,
			"ResTrInvModifyCount": self.ResTrInvModifyCount,
			"ResTrInvPrintCount": self.ResTrInvPrintCount,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_trans_inv_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_trans_inv_line"
	ResTrInvLineId = db.Column("ResTrInvLineId",db.Integer,nullable=False,primary_key=True)
	ResTrInvId = db.Column("ResTrInvId",db.Integer,db.ForeignKey("tbl_dk_res_trans_inv.ResTrInvId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column("LastVendorId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResTrInvLineDesc = db.Column("ResTrInvLineDesc",db.String(500))
	ResTrInvLineAmount = db.Column("ResTrInvLineAmount",db.Float,default=0.0)
	ResTrInvLinePrice = db.Column("ResTrInvLinePrice",db.Float,default=0.0)
	ResTrInvLineTotal = db.Column("ResTrInvLineTotal",db.Float,default=0.0)
	ResTrInvLineExpenseAmount = db.Column("ResTrInvLineExpenseAmount",db.Float,default=0.0)
	ResTrInvLineTaxAmount = db.Column("ResTrInvLineTaxAmount",db.Float,default=0.0)
	ResTrInvLineFTotal = db.Column("ResTrInvLineFTotal",db.Float,default=0.0)
	ResTrInvLineDate = db.Column("ResTrInvLineDate",db.DateTime)
	Res_transaction = db.relationship("Res_transaction",backref='res_trans_inv_line',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResTrInvLineId": self.ResTrInvLineId,
			"ResTrInvId": self.ResTrInvId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"LastVendorId": self.LastVendorId,
			"ResTrInvLineDesc": self.ResTrInvLineDesc,
			"ResTrInvLineAmount": self.ResTrInvLineAmount,
			"ResTrInvLinePrice": self.ResTrInvLinePrice,
			"ResTrInvLineTotal": self.ResTrInvLineTotal,
			"ResTrInvLineExpenseAmount": self.ResTrInvLineExpenseAmount,
			"ResTrInvLineTaxAmount": self.ResTrInvLineTaxAmount,
			"ResTrInvLineFTotal": self.ResTrInvLineFTotal,
			"ResTrInvLineDate": self.ResTrInvLineDate,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_trans_inv_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_trans_inv_type"
	ResTrInvTypeId = db.Column("ResTrInvTypeId",db.Integer,nullable=False,primary_key=True)
	ResTrInvName_tkTM = db.Column("ResTrInvName_tkTM",db.String(100),nullable=False)
	ResTrInvDesc_tkTM = db.Column("ResTrInvDesc_tkTM",db.String(500))
	ResTrInvName_ruRU = db.Column("ResTrInvName_ruRU",db.String(100))
	ResTrInvDesc_ruRU = db.Column("ResTrInvDesc_ruRU",db.String(500))
	ResTrInvName_enUS = db.Column("ResTrInvName_enUS",db.String(100))
	ResTrInvDesc_enUS = db.Column("ResTrInvDesc_enUS",db.String(500))
	Res_trans_inv = db.relationship("Res_trans_inv",backref='res_trans_inv_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResTrInvTypeId": self.ResTrInvTypeId,
			"ResTrInvName_tkTM": self.ResTrInvName_tkTM,
			"ResTrInvDesc_tkTM": self.ResTrInvDesc_tkTM,
			"ResTrInvName_ruRU": self.ResTrInvName_ruRU,
			"ResTrInvDesc_ruRU": self.ResTrInvDesc_ruRU,
			"ResTrInvName_enUS": self.ResTrInvName_enUS,
			"ResTrInvDesc_enUS": self.ResTrInvDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_trans_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_trans_type"
	ResTransTypeId = db.Column("ResTransTypeId",db.Integer,nullable=False,primary_key=True)
	ResTransTypeName_tkTM = db.Column("ResTransTypeName_tkTM",db.String(100),nullable=False)
	ResTransTypeDesc_tkTM = db.Column("ResTransTypeDesc_tkTM",db.String(500))
	ResTransTypeName_ruRU = db.Column("ResTransTypeName_ruRU",db.String(100))
	ResTransTypeDesc_ruRU = db.Column("ResTransTypeDesc_ruRU",db.String(500))
	ResTransTypeName_enUS = db.Column("ResTransTypeName_enUS",db.String(100))
	ResTransTypeDesc_enUS = db.Column("ResTransTypeDesc_enUS",db.String(500))
	Res_transaction = db.relationship("Res_transaction",backref='res_trans_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResTransTypeId": self.ResTransTypeId,
			"ResTransTypeName_tkTM": self.ResTransTypeName_tkTM,
			"ResTransTypeDesc_tkTM": self.ResTransTypeDesc_tkTM,
			"ResTransTypeName_ruRU": self.ResTransTypeName_ruRU,
			"ResTransTypeDesc_ruRU": self.ResTransTypeDesc_ruRU,
			"ResTransTypeName_enUS": self.ResTransTypeName_enUS,
			"ResTransTypeDesc_enUS": self.ResTransTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_transaction(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_transaction"
	ResTransId = db.Column("ResTransId",db.Integer,nullable=False,primary_key=True)
	ResTransTypeId = db.Column("ResTransTypeId",db.Integer,db.ForeignKey("tbl_dk_res_trans_type.ResTransTypeId"))
	InvLineId = db.Column("InvLineId",db.Integer,db.ForeignKey("tbl_dk_inv_line.InvLineId"))
	ResTrInvLineId = db.Column("ResTrInvLineId",db.Integer,db.ForeignKey("tbl_dk_res_trans_inv_line.ResTrInvLineId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	WhId = db.Column("WhId",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResTransName = db.Column("ResTransName",db.String(100),nullable=False)
	ResTransDesc = db.Column("ResTransDesc",db.String(500))
	ResTransAmount = db.Column("ResTransAmount",db.Float,default=0.0)
	ResTransPrice = db.Column("ResTransPrice",db.Float,default=0.0)
	ResTransFTotalPrice = db.Column("ResTransFTotalPrice",db.Float,default=0.0)
	ResTransResBalance = db.Column("ResTransResBalance",db.Float,default=0.0)
	ResTransDate = db.Column("ResTransDate",db.DateTime)
	ResTransPurchAvgPrice = db.Column("ResTransPurchAvgPrice",db.Float,default=0.0)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ResTransId": self.ResTransId,
			"ResTransTypeId": self.ResTransTypeId,
			"InvLineId": self.InvLineId,
			"ResTrInvLineId": self.ResTrInvLineId,
			"CurrencyId": self.CurrencyId,
			"UnitId": self.UnitId,
			"WhId": self.WhId,
			"ResId": self.ResId,
			"ResTransName": self.ResTransName,
			"ResTransDesc": self.ResTransDesc,
			"ResTransAmount": self.ResTransAmount,
			"ResTransPrice": self.ResTransPrice,
			"ResTransFTotalPrice": self.ResTransFTotalPrice,
			"ResTransResBalance": self.ResTransResBalance,
			"ResTransDate": self.ResTransDate,
			"ResTransPurchAvgPrice": self.ResTransPurchAvgPrice,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_translations(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_translations"
	ResTransId = db.Column("ResTransId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LangId = db.Column("LangId",db.Integer,db.ForeignKey("tbl_dk_language.LangId"))
	ResName = db.Column("ResName",db.String(255))
	ResDesc = db.Column("ResDesc",db.String(500))
	ResFullDesc = db.Column("ResFullDesc",db.String(1500))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"resTransId": self.ResTransId,
			"resId": self.ResId,
			"langId": self.LangId,
			"resNameTrans": self.ResName,
			"resDescTrans": self.ResDesc,
			"resFullDescTrans": self.ResFullDesc
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"ResTransId": self.ResTransId,
			"ResId": self.ResId,
			"LangId": self.LangId,
			"ResName": self.ResName,
			"ResDesc": self.ResDesc,
			"ResFullDesc": self.ResFullDesc
		}
		return json_data


class Res_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_type"
	ResTypeId = db.Column("ResTypeId",db.Integer,nullable=False,primary_key=True)
	ResTypeName_tkTM = db.Column("ResTypeName_tkTM",db.String(100))
	ResTypeDesc_tkTM = db.Column("ResTypeDesc_tkTM",db.String(500))
	ResTypeName_ruRU = db.Column("ResTypeName_ruRU",db.String(100))
	ResTypeDesc_ruRU = db.Column("ResTypeDesc_ruRU",db.String(500))
	ResTypeName_enUS = db.Column("ResTypeName_enUS",db.String(100))
	ResTypeDesc_enUS = db.Column("ResTypeDesc_enUS",db.String(500))
	Resource = db.relationship("Resource",backref='res_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"ResTypeId": self.ResTypeId,
			"ResTypeName_tkTM": self.ResTypeName_tkTM,
			"ResTypeDesc_tkTM": self.ResTypeDesc_tkTM,
			"ResTypeName_ruRU": self.ResTypeName_ruRU,
			"ResTypeDesc_ruRU": self.ResTypeDesc_ruRU,
			"ResTypeName_enUS": self.ResTypeName_enUS,
			"ResTypeDesc_enUS": self.ResTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Res_unit(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_unit"
	ResUnitId = db.Column("ResUnitId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResUnitUnitId = db.Column("ResUnitUnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResUnitConvAmount = db.Column("ResUnitConvAmount",db.Float,nullable=False)
	ResUnitConvTypeId = db.Column("ResUnitConvTypeId",db.Integer,nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"resUnitId": self.ResUnitId,
			"resId": self.ResId,
			"resUnitUnitId": self.ResUnitUnitId,
			"resUnitConvAmount": self.ResUnitConvAmount,
			"resUnitConvTypeId": self.ResUnitConvTypeId
		}
		return json_data

	def to_json_api(self):
		json_data = {
			"ResUnitId": self.ResUnitId,
			"ResId": self.ResId,
			"ResUnitUnitId": self.ResUnitUnitId,
			"ResUnitConvAmount": self.ResUnitConvAmount,
			"ResUnitConvTypeId": self.ResUnitConvTypeId
		}
		return json_data


class Rp_acc_resource(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rp_acc_resource"
	RpAccResId = db.Column("RpAccResId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"RpAccResId": self.RpAccResId,
			"RpAccId": self.RpAccId,
			"ResId": self.ResId,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Rp_acc_trans_total(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rp_acc_trans_total"
	RpAccTrTotId = db.Column("RpAccTrTotId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccTrTotBalance = db.Column("RpAccTrTotBalance",db.Float,default=0.0)
	RpAccTrTotDebit = db.Column("RpAccTrTotDebit",db.Float,default=0.0)
	RpAccTrTotCredit = db.Column("RpAccTrTotCredit",db.Float,default=0.0)
	RpAccTrTotLastTrDate = db.Column("RpAccTrTotLastTrDate",db.DateTime,default=datetime.now)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"RpAccTrTotId": self.RpAccTrTotId,
			"RpAccId": self.RpAccId,
			"CurrencyId": self.CurrencyId,
			"RpAccTrTotBalance": self.RpAccTrTotBalance,
			"RpAccTrTotDebit": self.RpAccTrTotDebit,
			"RpAccTrTotCredit": self.RpAccTrTotCredit,
			"RpAccTrTotLastTrDate": apiDataFormat(self.RpAccTrTotLastTrDate),
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Rp_acc_transaction(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rp_acc_transaction"
	RpAccTransId = db.Column("RpAccTransId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	TransTypeId = db.Column("TransTypeId",db.Integer,db.ForeignKey("tbl_dk_transaction_type.TransTypeId"))
	InvId = db.Column("InvId",db.Integer,db.ForeignKey("tbl_dk_invoice.InvId"))
	ResTransInvId = db.Column("ResTransInvId",db.Integer,db.ForeignKey("tbl_dk_res_trans_inv.ResTrInvId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	RpAccTransName = db.Column("RpAccTransName",db.String(100),nullable=False)
	RpAccTransCode = db.Column("RpAccTransCode",db.String(100))
	RpAccTransDate = db.Column("RpAccTransDate",db.DateTime)
	RpAccTransDebit = db.Column("RpAccTransDebit",db.Float,default=0.0)
	RpAccTransCredit = db.Column("RpAccTransCredit",db.Float,default=0.0)
	RpAccTransTotal = db.Column("RpAccTransTotal",db.Float,default=0.0)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"RpAccTransId": self.RpAccTransId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WpId": self.WpId,
			"TransTypeId": self.TransTypeId,
			"InvId": self.InvId,
			"ResTransInvId": self.ResTransInvId,
			"RpAccId": self.RpAccId,
			"CurrencyId": self.CurrencyId,
			"RpAccTransName": self.RpAccTransName,
			"RpAccTransCode": self.RpAccTransCode,
			"RpAccTransDate": self.RpAccTransDate,
			"RpAccTransDebit": self.RpAccTransDebit,
			"RpAccTransCredit": self.RpAccTransCredit,
			"RpAccTransTotal": self.RpAccTransTotal,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Sale_agr_res_price(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sale_agr_res_price"
	SAResPriceId = db.Column("SAResPriceId",db.Integer,nullable=False,primary_key=True)
	SaleAgrId = db.Column("SaleAgrId",db.Integer,db.ForeignKey("tbl_dk_sale_agreement.SaleAgrId"))
	ResPriceTypeId = db.Column("ResPriceTypeId",db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SAResPriceRegNo = db.Column("SAResPriceRegNo",db.String(100),nullable=False)
	SAResPriceValue = db.Column("SAResPriceValue",db.Float,default=0.0)
	SAPriceStartDate = db.Column("SAPriceStartDate",db.DateTime)
	SAPriceEndDate = db.Column("SAPriceEndDate",db.DateTime)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"SAResPriceId": self.SAResPriceId,
			"SaleAgrId": self.SaleAgrId,
			"ResPriceTypeId": self.ResPriceTypeId,
			"UnitId": self.UnitId,
			"CurrencyId": self.CurrencyId,
			"ResId": self.ResId,
			"SAResPriceRegNo": self.SAResPriceRegNo,
			"SAResPriceValue": self.SAResPriceValue,
			"SAPriceStartDate": self.SAPriceStartDate,
			"SAPriceEndDate": self.SAPriceEndDate,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Sale_agreement(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sale_agreement"
	SaleAgrId = db.Column("SaleAgrId",db.Integer,nullable=False,primary_key=True)
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	SaleAgrName = db.Column("SaleAgrName",db.String(100),nullable=False)
	SaleAgrDesc = db.Column("SaleAgrDesc",db.String(500))
	SaleAgrMinOrderPrice = db.Column("SaleAgrMinOrderPrice",db.Float,default=0.0)
	SaleAgrDiscPerc = db.Column("SaleAgrDiscPerc",db.Float,default=0.0)
	SaleAgrMaxDiscPerc = db.Column("SaleAgrMaxDiscPerc",db.Float,default=0.0)
	SaleAgrTaxPerc = db.Column("SaleAgrTaxPerc",db.Float,default=0.0)
	SaleAgrTaxAmount = db.Column("SaleAgrTaxAmount",db.Float,default=0.0)
	SaleAgrUseOwnPriceList = db.Column("SaleAgrUseOwnPriceList",db.Boolean,default=False)
	Sale_card = db.relationship("Sale_card",backref='sale_agreement',lazy=True)
	Sale_agr_res_price = db.relationship("Sale_agr_res_price",backref='sale_agreement',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"SaleAgrId": self.SaleAgrId,
			"CurrencyId": self.CurrencyId,
			"SaleAgrName": self.SaleAgrName,
			"SaleAgrDesc": self.SaleAgrDesc,
			"SaleAgrMinOrderPrice": self.SaleAgrMinOrderPrice,
			"SaleAgrDiscPerc": self.SaleAgrDiscPerc,
			"SaleAgrMaxDiscPerc": self.SaleAgrMaxDiscPerc,
			"SaleAgrTaxPerc": self.SaleAgrTaxPerc,
			"SaleAgrTaxAmount": self.SaleAgrTaxAmount,
			"SaleAgrUseOwnPriceList": self.SaleAgrUseOwnPriceList,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Sale_card(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sale_card"
	SaleCardId = db.Column("SaleCardId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WpId = db.Column("WpId",db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	SaleAgrId = db.Column("SaleAgrId",db.Integer,db.ForeignKey("tbl_dk_sale_agreement.SaleAgrId"))
	ResPriceGroupId = db.Column("ResPriceGroupId",db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	ResDiscId = db.Column("ResDiscId",db.Integer,db.ForeignKey("tbl_dk_res_discount.ResDiscId"))
	SaleCardStatusId = db.Column("SaleCardStatusId",db.Integer,db.ForeignKey("tbl_dk_sale_card_status.SaleCardStatusId"))
	SaleCardRegNo = db.Column("SaleCardRegNo",db.String(100),nullable=False)
	SaleCardName = db.Column("SaleCardName",db.String(100),nullable=False)
	SaleCardDesc = db.Column("SaleCardDesc",db.String(500))
	SaleCardStartDate = db.Column("SaleCardStartDate",db.DateTime,default=datetime.now)
	SaleCardEndDate = db.Column("SaleCardEndDate",db.DateTime,default=datetime.now)
	SaleCardMinSaleAmount = db.Column("SaleCardMinSaleAmount",db.Float,default=0.0)
	SaleCardMaxSaleAmount = db.Column("SaleCardMaxSaleAmount",db.Float,default=0.0)
	SaleCardMinSalePrice = db.Column("SaleCardMinSalePrice",db.Float,default=0.0)
	SaleCardMaxSalePrice = db.Column("SaleCardMaxSalePrice",db.Float,default=0.0)
	SaleCardMaxManualDiscPerc = db.Column("SaleCardMaxManualDiscPerc",db.Float,default=0.0)
	SaleCardIsPayable = db.Column("SaleCardIsPayable",db.Boolean,default=True)
	SaleCardCustName = db.Column("SaleCardCustName",db.String(100))
	SaleCardCustBirthDate = db.Column("SaleCardCustBirthDate",db.String(100))
	SaleCardCustTel = db.Column("SaleCardCustTel",db.String(100))
	SaleCardCustEmail = db.Column("SaleCardCustEmail",db.String(100))
	SaleCardCustAddress = db.Column("SaleCardCustAddress",db.String(100))
	Res_discount = db.relationship("Res_discount",backref='sale_card',foreign_keys='Res_discount.SaleCardId',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"SaleCardId": self.SaleCardId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WpId": self.WpId,
			"RpAccId": self.RpAccId,
			"CurrencyId": self.CurrencyId,
			"SaleAgrId": self.SaleAgrId,
			"ResPriceGroupId": self.ResPriceGroupId,
			"ResDiscId": self.ResDiscId,
			"SaleCardStatusId": self.SaleCardStatusId,
			"SaleCardRegNo": self.SaleCardRegNo,
			"SaleCardName": self.SaleCardName,
			"SaleCardDesc": self.SaleCardDesc,
			"SaleCardStartDate": self.SaleCardStartDate,
			"SaleCardEndDate": self.SaleCardEndDate,
			"SaleCardMinSaleAmount": self.SaleCardMinSaleAmount,
			"SaleCardMaxSaleAmount": self.SaleCardMaxSaleAmount,
			"SaleCardMinSalePrice": self.SaleCardMinSalePrice,
			"SaleCardMaxSalePrice": self.SaleCardMaxSalePrice,
			"SaleCardMaxManualDiscPerc": self.SaleCardMaxManualDiscPerc,
			"SaleCardIsPayable": self.SaleCardIsPayable,
			"SaleCardCustName": self.SaleCardCustName,
			"SaleCardCustBirthDate": self.SaleCardCustBirthDate,
			"SaleCardCustTel": self.SaleCardCustTel,
			"SaleCardCustEmail": self.SaleCardCustEmail,
			"SaleCardCustAddress": self.SaleCardCustAddress,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Sale_card_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_sale_card_status"
	SaleCardStatusId = db.Column("SaleCardStatusId",db.Integer,nullable=False,primary_key=True)
	SaleCardStatusName_tkTM = db.Column("SaleCardStatusName_tkTM",db.String(100))
	SaleCardStatusDesc_tkTM = db.Column("SaleCardStatusDesc_tkTM",db.String(500))
	SaleCardStatusName_ruRU = db.Column("SaleCardStatusName_ruRU",db.String(100))
	SaleCardStatusDesc_ruRU = db.Column("SaleCardStatusDesc_ruRU",db.String(500))
	SaleCardStatusName_enUS = db.Column("SaleCardStatusName_enUS",db.String(100))
	SaleCardStatusDesc_enUS = db.Column("SaleCardStatusDesc_enUS",db.String(500))
	Sale_card = db.relationship("Sale_card",backref='sale_card_status',lazy=True)

	def to_json_api(self):
		json_data = {
			"SaleCardStatusId": self.SaleCardStatusId,
			"SaleCardStatusName_tkTM": self.SaleCardStatusName_tkTM,
			"SaleCardStatusDesc_tkTM": self.SaleCardStatusDesc_tkTM,
			"SaleCardStatusName_ruRU": self.SaleCardStatusName_ruRU,
			"SaleCardStatusDesc_ruRU": self.SaleCardStatusDesc_ruRU,
			"SaleCardStatusName_enUS": self.SaleCardStatusName_enUS,
			"SaleCardStatusDesc_enUS": self.SaleCardStatusDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Production(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_production"
	ProdId = db.Column("ProdId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WhIdIn = db.Column("WhIdIn",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	WhIdOut = db.Column("WhIdOut",db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ProdName = db.Column("ProdName",db.String(100),nullable=False)
	ProdDesc = db.Column("ProdDesc",db.String(500),default='')
	ProdTime = db.Column("ProdTime",db.Float)
	ProdCostPrice = db.Column("ProdCostPrice",db.Float)
	Production_line = db.relationship("Production_line",backref='production',lazy=True)
	Image = db.relationship("Image",backref='production',lazy=True)
	Translations = db.relationship("Translations",backref='production',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ProdId": self.ProdId,
			"CId": self.CId,
			"DivId": self.DivId,
			"WhIdIn": self.WhIdIn,
			"WhIdOut": self.WhIdOut,
			"ResId": self.ResId,
			"ProdName": self.ProdName,
			"ProdDesc": self.ProdDesc,
			"ProdTime": self.ProdTime,
			"ProdCostPrice": self.ProdCostPrice,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Production_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_production_line"
	ProdLineId = db.Column("ProdLineId",db.Integer,nullable=False,primary_key=True)
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	UnitId = db.Column("UnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ProdLineAmount = db.Column("ProdLineAmount",db.Float,nullable=False,default=0)
	ProdLinePrice = db.Column("ProdLinePrice",db.Float)
	ProdLineDesc = db.Column("ProdLineDesc",db.String(500),default='')

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"ProdLineId": self.ProdLineId,
			"ProdId": self.ProdId,
			"UnitId": self.UnitId,
			"ResId": self.ResId,
			"ProdLineAmount": self.ProdLineAmount,
			"ProdLinePrice": self.ProdLinePrice,
			"ProdLineDesc": self.ProdLineDesc,			
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Rating(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rating"
	RtId = db.Column("RtId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RtRemark = db.Column("RtRemark",db.String(500),default='')
	RtRatingValue = db.Column("RtRatingValue",db.Float,nullable=False,default=0)
	RtValidated = db.Column("RtValidated",db.Boolean,default=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"RtId": self.RtId,
			"CId": self.CId,
			"DivId": self.DivId,
			"UId": self.UId,
			"ResId": self.ResId,
			"RpAccId": self.RpAccId,
			"EmpId": self.EmpId,
			"RtRemark": self.RtRemark,
			"RtRatingValue": self.RtRatingValue,
			"RtValidated": self.RtValidated,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Wish(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_wish"
	WishId = db.Column("WishId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"WishId": self.WishId,
			"CId": self.CId,
			"DivId": self.DivId,
			"UId": self.UId,
			"ResId": self.ResId,
			"RpAccId": self.RpAccId,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Transaction_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_transaction_type"
	TransTypeId = db.Column("TransTypeId",db.Integer,nullable=False,primary_key=True)
	TransTypeName = db.Column("TransTypeName",db.String(100),nullable=False)
	TransTypeDesc = db.Column("TransTypeDesc",db.String(500))
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='transaction_type',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"TransTypeId": self.TransTypeId,
			"TransTypeName": self.TransTypeName,
			"TransTypeDesc": self.TransTypeDesc,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data


class Work_period(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_work_period"
	WpId = db.Column("WpId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	CurrencyId = db.Column("CurrencyId",db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	WpStartDate = db.Column("WpStartDate",db.DateTime)
	WpEndDate = db.Column("WpEndDate",db.DateTime)
	WpIsDefault = db.Column("WpIsDefault",db.Boolean,default=False)
	Rp_acc = db.relationship("Rp_acc",backref='work_period',lazy=True)
	Invoice = db.relationship("Invoice",backref='work_period',lazy=True)
	Order_inv = db.relationship("Order_inv",backref='work_period',lazy=True)
	Res_total = db.relationship("Res_total",backref='work_period',lazy=True)
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='work_period',lazy=True)
	Sale_card = db.relationship("Sale_card",backref='work_period',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		json_data = {
			"WpId": self.WpId,
			"CId": self.CId,
			"DivId": self.DivId,
			"CurrencyId": self.CurrencyId,
			"WpStartDate": self.WpStartDate,
			"WpEndDate": self.WpEndDate,
			"WpIsDefault": self.WpIsDefault,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data