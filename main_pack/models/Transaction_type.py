
class Transaction_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_transaction_type"
	TransTypeId = db.Column("TransTypeId",db.Integer,nullable=False,primary_key=True)
	TransTypeName = db.Column("TransTypeName",db.String(100),nullable=False)
	TransTypeDesc = db.Column("TransTypeDesc",db.String(500))
	Rp_acc_transaction = db.relationship("Rp_acc_transaction",backref='transaction_type',lazy=True)

	def to_json_api(self):
		json_data = {
			"TransTypeId": self.TransTypeId,
			"TransTypeName": self.TransTypeName,
			"TransTypeDesc": self.TransTypeDesc
		}
		return json_data
