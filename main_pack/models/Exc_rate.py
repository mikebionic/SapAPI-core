
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