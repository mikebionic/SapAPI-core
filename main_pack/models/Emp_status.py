
class Emp_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_emp_status"
	EmpStatId = db.Column("EmpStatId",db.Integer,nullable=False,primary_key=True)
	EmpStatName_tkTM = db.Column("EmpStatName_tkTM",db.String(100))#,nullable=False)
	EmpStatDesc_tkTM = db.Column("EmpStatDesc_tkTM",db.String(500))
	EmpStatName_ruRU = db.Column("EmpStatName_ruRU",db.String(100))#,nullable=False)
	EmpStatDesc_ruRU = db.Column("EmpStatDesc_ruRU",db.String(500))
	EmpStatName_enUS = db.Column("EmpStatName_enUS",db.String(100))#,nullable=False)
	EmpStatDesc_enUS = db.Column("EmpStatDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='emp_status',lazy=True)

	def to_json(self):
		json_data = {
			"EmpStatId": self.EmpStatId,
			"EmpStatName_tkTM": self.EmpStatName_tkTM,
			"EmpStatDesc_tkTM": self.EmpStatDesc_tkTM,
			"EmpStatName_ruRU": self.EmpStatName_ruRU,
			"EmpStatDesc_ruRU": self.EmpStatDesc_ruRU,
			"EmpStatName_enUS": self.EmpStatName_enUS,
			"EmpStatDesc_enUS": self.EmpStatDesc_enUS
		}
		return json_data

