from main_pack import db
from datetime import datetime
from flask_login import current_user
from main_pack.models.base.models import CreatedModifiedInfo, AddInf

class Barcode(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_barcode"
	BarcodeId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivisionId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BarcodeVal = db.Column(db.String(100),nullable=False)

class Brand(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_brand"
	BrandId = db.Column(db.Integer,nullable=False,primary_key=True)
	BrandName = db.Column(db.String(100),nullable=False)
	BrandDesc = db.Column(db.String(100))
	Resource = db.relationship('Resource',backref='brand',lazy=True)

class Color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_color"
	ColorId = db.Column(db.Integer,nullable=False,primary_key=True)
	ColorName = db.Column(db.String(100),nullable=False)
	ColorDesc = db.Column(db.String(500))
	ColorCode = db.Column(db.String(100))
	Res_color = db.relationship('Res_color',backref='color',lazy=True)

class Res_color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_color"
	RcId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ColorId = db.Column(db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))

class Res_size(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_size"
	RsId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SizeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_size.SizeId"))

class Res_translations(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_translations"
	ResTansId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LangId = db.Column(db.Integer,db.ForeignKey("tbl_dk_language.LangId"))
	ResName = db.Column(db.String(255))
	ResDesc = db.Column(db.String(500))
	ResFullDesc = db.Column(db.String(1500))

class Res_unit(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_unit"
	ResUnitId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResUnitUnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResUnitConvAmount = db.Column(db.Float,nullable=False)
	ResUnitConvTypeId = db.Column(db.Integer,nullable=False)

class Size(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_size"
	SizeId = db.Column(db.Integer,nullable=False,primary_key=True)
	SizeName = db.Column(db.String(100),nullable=False)
	SizeDesc = db.Column(db.String(500))
	SizeTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_size_type.SizeTypeId"))
	Res_size = db.relationship('Res_size',backref='size',lazy=True)

class Size_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_size_type"
	SizeTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	SizeTypeName = db.Column(db.String(100),nullable=False)
	SizeTypeDesc = db.Column(db.String(500))
	Size = db.relationship('Size',backref='size_type',lazy=True)

class Unit(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_unit"
	UnitId = db.Column(db.Integer,nullable=False,primary_key=True)
	UnitName = db.Column(db.String(100),nullable=False)
	UnitDesc = db.Column(db.String(100))
	Res_unit = db.relationship('Res_unit',backref='unit',lazy=True)
	Barcode = db.relationship('Barcode',backref='unit',lazy=True)
	Resource = db.relationship('Resource',backref='unit',lazy=True)

class Usage_status(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_usage_status"
	UsageStatusId = db.Column(db.Integer,nullable=False,primary_key=True)
	UsageStatusName = db.Column(db.String(100),nullable=False)
	UsageStatusDesc = db.Column(db.String(500))
	Resource = db.relationship('Resource',backref='usage_status',lazy=True)