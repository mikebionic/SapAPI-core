

class Rp_acc_resource(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rp_acc_resource"
	RpAccResId = db.Column("RpAccResId",db.Integer,nullable=False,primary_key=True)
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))

	def to_json_api(self):
		json_data = {
			"RpAccResId": self.RpAccResId,
			"RpAccId": self.RpAccId,
			"ResId": self.ResId
		}
		return json_data

