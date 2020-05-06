
class Resource(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_resource"
	ResId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResCatId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BrandId = db.Column(db.Integer,db.ForeignKey("tbl_dk_brand.BrandId"))
	UsageStatusId = db.Column(db.Integer,db.ForeignKey("tbl_dk_usage_status.UsageStatusId"))
	ResourceTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource_type.ResourceTypeId"))
	ResMainImgId = db.Column(db.Integer,default=0)
	ResMakerId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource_maker.ResMakerId"))
	ResLastVendorId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResRegNo = db.Column(db.String(50),nullable=False)
	ResName = db.Column(db.String(255),nullable=False)
	ResDesc = db.Column(db.String(500))
	ResFullDesc = db.Column(db.String(1500))
	ResWidth = db.Column(db.Float,default=0)
	ResHeight = db.Column(db.Float,default=0)
	ResLength = db.Column(db.Float,default=0)
	ResWeight = db.Column(db.Float,default=0)
	ResProductionOnSale = db.Column(db.Boolean,default=False)
	ResMinSaleAmount = db.Column(db.Float,default=0)
	ResMaxSaleAmount = db.Column(db.Float,default=0)
	ResMinSalePrice = db.Column(db.Float,default=0)
	ResMaxSalePrice = db.Column(db.Float,default=0)
	Image = db.relationship('Image',backref='resource',lazy=True)
	Barcode = db.relationship('Barcode',backref='resource',lazy=True)
	Res_color = db.relationship('Res_color',backref='resource',lazy=True)
	Res_size = db.relationship('Res_size',backref='resource',lazy=True)
	Res_translations = db.relationship('Res_translations',backref='resource',lazy=True)
	Unit = db.relationship('Unit',backref='resource',lazy=True)
	Res_unit = db.relationship('Res_unit',backref='resource',lazy=True)
	Inv_line = db.relationship('Inv_line',backref='resource',lazy=True)
	Inv_line_det = db.relationship('Inv_line_det',backref='resource',lazy=True)	
	Order_inv_line = db.relationship('Order_inv_line',backref='resource',lazy=True)
	Res_price = db.relationship('Res_price',backref='resource',lazy=True)
	Res_total = db.relationship('Res_total',backref='resource',lazy=True)
	Res_trans_inv_line = db.relationship('Res_trans_inv_line',backref='resource',lazy=True)
	Res_transaction = db.relationship('Res_transaction',backref='resource',lazy=True)
	Rp_acc_resource = db.relationship('Rp_acc_resource',backref='resource',lazy=True)
	Sale_agr_res_price = db.relationship('Sale_agr_res_price',backref='resource',lazy=True)
	Res_discount = db.relationship('Res_discount',foreign_keys='Res_discount.SaleResId',backref='resource',lazy=True)
	Res_discount = db.relationship('Res_discount',foreign_keys='Res_discount.GiftResId',backref='resource',lazy=True)
	
	def to_json(self):
		json_resource = {
			'resourceId':self.ResId,
			'company':self.CId,
			'division':self.DivId,
			'resourceCategory':self.ResCatId,
			'unit':self.UnitId,
			'brand':self.BrandId,
			'usageStatus':self.UsageStatusId,
			'resourceType':self.ResourceTypeId,
			'mainImage':self.ResMainImgId,
			'resourceMaker':self.ResMakerId,
			'lastVendor':self.ResLastVendorId,
			'regNo':self.ResRegNo,
			'resourceName':self.ResName,
			'resourceDesc':self.ResDesc,
			'resourceFullDesc':self.ResFullDesc,
			'resourceWidth':self.ResWidth,
			'resourceHeight':self.ResHeight,
			'resourceLength':self.ResLength,
			'resourceWeight':self.ResWeight,
			'resourceOnSale':self.ResProductionOnSale,
			'resourceMinSaleAmount':self.ResMinSaleAmount,
			'resourceMaxSaleAmount':self.ResMaxSaleAmount,
			'resourceMinSalePrice':self.ResMinSalePrice,
			'resourceMaxSalePrice':self.ResMaxSalePrice
			}
		return json_resource
	
class Image(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_image"
	ImgId = db.Column(db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	FileName = db.Column(db.String(100))
	FileHash = db.Column(db.String(100))
	Image = db.Column(db.LargeBinary)

class Barcode(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_barcode"
	BarcodeId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	BarcodeVal = db.Column(db.String(100),nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json(self):
		json_barcode = {
			'barcodeId':self.BarcodeId,
			'companyId':self.CId,
			'divisionId':self.DivId,
			'resourceId':self.ResId,
			'unitId':self.UnitId,
			'barcodeVal':self.BarcodeVal
			}
		return json_barcode


class Unit(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_unit"
	UnitId = db.Column(db.Integer,nullable=False,primary_key=True)
	UnitName_tkTM = db.Column(db.String(100))
	UnitDesc_tkTM = db.Column(db.String(100))
	UnitName_ruRU = db.Column(db.String(100))
	UnitDesc_ruRU = db.Column(db.String(100))
	UnitName_enUS = db.Column(db.String(100))
	UnitDesc_enUS = db.Column(db.String(100))
	Res_unit = db.relationship('Res_unit',backref='unit',lazy=True)
	Barcode = db.relationship('Barcode',backref='unit',lazy=True)
	Resource = db.relationship('Resource',backref='unit',lazy=True)
	Inv_line = db.relationship('Inv_line',backref='unit',lazy=True)
	Order_inv_line = db.relationship('Order_inv_line',backref='unit',lazy=True)
	Res_price = db.relationship('Res_price',backref='unit',lazy=True)
	Res_trans_inv_line = db.relationship('Res_trans_inv_line',backref='unit',lazy=True)
	Res_transaction = db.relationship('Res_transaction',backref='unit',lazy=True)
	Sale_agr_res_price = db.relationship('Sale_agr_res_price',backref='unit',lazy=True)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

class Res_color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_color"
	RcId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ColorId = db.Column(db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

class Res_size(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_size"
	RsId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SizeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_size.SizeId"))

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

####################


class Res_discount(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_discount"
	ResDiscId = db.Column(db.Integer,nullable=False,primary_key=True)
	SaleCardId = db.Column(db.Integer,db.ForeignKey("tbl_dk_sale_card.SaleCardId"))
	ResDiscRegNo = db.Column(db.String(100),nullable=False)
	SaleResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SaleResAmount = db.Column(db.Float,default=0)
	DiscTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_discount_type.DiscTypeId"))
	DiscValue = db.Column(db.Float,default=0.0)
	DiscDesc = db.Column(db.String(500))
	ResDiscStartDate = db.Column(db.DateTime)
	ResDiscEndDate = db.Column(db.DateTime)
	ResDiscIsActive = db.Column(db.Boolean,default=True)
	GiftResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	GiftResAmount = db.Column(db.Float,default=0)
	GiftResDiscValue = db.Column(db.Float,default=0)
	Sale_card = db.relationship('Sale_card',backref='res_discount',foreign_keys='Sale_card.ResDiscId',lazy=True)

class Res_price(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_price"
	ResPriceId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResPriceTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ResPriceGroupId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_group.ResPriceGroupId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column(db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResPriceRegNo = db.Column(db.String(100),nullable=False)
	ResPriceValue = db.Column(db.Float,default=0)
	PriceStartDate = db.Column(db.DateTime)
	PriceEndDate = db.Column(db.DateTime)

class Res_total(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_total"
	ResTotId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	CurrencyId = db.Column(db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	WhId = db.Column(db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	WpId = db.Column(db.Integer,db.ForeignKey("tbl_dk_work_period.WpId"))
	ResTotBalance = db.Column(db.Float,default=0)
	ResTotInAmount = db.Column(db.Float,default=0)
	ResTotOutAmount = db.Column(db.Float,default=0)
	ResTotLastTrDate = db.Column(db.DateTime,default=datetime.now)
	ResTotPurchAvgPrice = db.Column(db.Float,default=0)


class Res_trans_inv_line(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_trans_inv_line"
	ResTrInvLineId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResTrInvId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_trans_inv.ResTrInvId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column(db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	LastVendorId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResTrInvLineDesc = db.Column(db.String(500))
	ResTrInvLineAmount = db.Column(db.Float,default=0)
	ResTrInvLinePrice = db.Column(db.Float,default=0)
	ResTrInvLineTotal = db.Column(db.Float,default=0)
	ResTrInvLineExpenseAmount = db.Column(db.Float,default=0)
	ResTrInvLineTaxAmount = db.Column(db.Float,default=0)
	ResTrInvLineFTotal = db.Column(db.Float,default=0)
	ResTrInvLineDate = db.Column(db.DateTime)
	Res_transaction = db.relationship('Res_transaction',backref='res_trans_inv_line',lazy=True)

class Res_transaction(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_transaction"
	ResTransId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResTransTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_trans_type.ResTransTypeId"))
	InvLineId = db.Column(db.Integer,db.ForeignKey("tbl_dk_inv_line.InvLineId"))
	ResTrInvLineId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_trans_inv_line.ResTrInvLineId"))
	CurrencyId = db.Column(db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	WhId = db.Column(db.Integer,db.ForeignKey("tbl_dk_warehouse.WhId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResTransName = db.Column(db.String(100),nullable=False)
	ResTransDesc = db.Column(db.String(500))
	ResTransAmount = db.Column(db.Float,default=0)
	ResTransPrice = db.Column(db.Float,default=0)
	ResTransFTotalPrice = db.Column(db.Float,default=0)
	ResTransResBalance = db.Column(db.Float,default=0)
	ResTransDate = db.Column(db.DateTime)
	ResTransPurchAvgPrice = db.Column(db.Float,default=0)




class Res_unit(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_res_unit"
	ResUnitId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResUnitUnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResUnitConvAmount = db.Column(db.Float,nullable=False)
	ResUnitConvTypeId = db.Column(db.Integer,nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)


class Rp_acc_resource(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_rp_acc_resource"
	RpAccResId = db.Column(db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column(db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))


class Sale_agr_res_price(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_sale_agr_res_price"
	SAResPriceId = db.Column(db.Integer,nullable=False,primary_key=True)
	SaleAgrId = db.Column(db.Integer,db.ForeignKey("tbl_dk_sale_agreement.SaleAgrId"))
	ResPriceTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	UnitId = db.Column(db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	CurrencyId = db.Column(db.Integer,db.ForeignKey("tbl_dk_currency.CurrencyId"))
	ResId = db.Column(db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SAResPriceRegNo = db.Column(db.String(100),nullable=False)
	SAResPriceValue = db.Column(db.Float,default=0)
	SAPriceStartDate = db.Column(db.DateTime)
	SAPriceEndDate = db.Column(db.DateTime)
