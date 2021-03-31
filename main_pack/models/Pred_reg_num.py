

class Pred_reg_num(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_pred_regnum"
	PredRegNumId = db.Column("PredRegNumId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,db.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	RegNum = db.Column("RegNum",db.String(100),nullable=False)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)

	def to_json_api(self):
		pred_regnum = {
			"PredRegNumId": self.PredRegNumId,			
			"RegNumTypeId": self.RegNumTypeId,
			"RegNum": self.RegNum,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return pred_regnum