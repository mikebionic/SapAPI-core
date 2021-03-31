
class Res_color(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_color"
	RcId = db.Column("RcId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ColorId = db.Column("ColorId",db.Integer,db.ForeignKey("tbl_dk_color.ColorId"))

	def to_json_api(self):
		json_data = {
			"RcId": self.RcId,
			"ResId": self.ResId,
			"ColorId": self.ColorId
		}
		return json_data