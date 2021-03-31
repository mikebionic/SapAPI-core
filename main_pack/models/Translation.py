

class Translation(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_translations"
	TranslId = db.Column("TranslId",db.Integer,nullable=False,primary_key=True)
	ResCatId = db.Column("ResCatId",db.Integer,db.ForeignKey("tbl_dk_res_category.ResCatId"))
	ColorId = db.Column("ColorId",db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))
	ProdId = db.Column("ProdId",db.Integer,db.ForeignKey("tbl_dk_production.ProdId"))
	SlImgId = db.Column("SlImgId",db.Integer,db.ForeignKey("tbl_dk_sl_image.SlImgId"))
	TransMain = db.Column("TransMain",db.String(500))
	TransDesc = db.Column("TransDesc",db.String(1000))
