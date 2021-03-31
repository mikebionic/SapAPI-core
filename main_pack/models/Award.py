

class Award(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_award"
	AwardId = db.Column("AwardId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	AwardName = db.Column("AwardName",db.String(100),nullable=False)
	AwardDesc = db.Column("AwardDesc",db.String(500))
	AwardRecievedDate = db.Column("AwardRecievedDate",db.DateTime)
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if value is not None:
				if hasattr(self, key):
					setattr(self, key, value)
	def to_json(self):
		json_data = {
			"awardId": self.AwardId,
			"empId": self.EmpId,
			"awardName": self.AwardName,
			"awardDesc": self.AwardDesc,
			"awardRecievedDate": self.AwardRecievedDate
		}
		return json_data
