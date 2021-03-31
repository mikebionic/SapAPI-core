
class Res_size(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_size"
	RsId = db.Column("RsId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	SizeId = db.Column("SizeId",db.Integer,db.ForeignKey("tbl_dk_size.SizeId"))

	def to_json_api(self):
		json_data = {
			"RsId": self.RsId,
			"ResId": self.ResId,
			"SizeId": self.SizeId
		}
		return json_data

