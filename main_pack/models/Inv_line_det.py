
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
