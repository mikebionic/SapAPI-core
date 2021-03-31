
class Work_history(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_work_history"
	WorkHistId = db.Column("WorkHistId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	WorkHistoryWorkPlace = db.Column("WorkHistoryWorkPlace",db.String(100),nullable=False)
	WorkHistoryWorkDesc = db.Column("WorkHistoryWorkDesc",db.String(500))
	WorkHistoryWorkDept = db.Column("WorkHistoryWorkDept",db.String(255))
	WorkHistoryWorkPos = db.Column("WorkHistoryWorkPos",db.String(255))
	WorkHistoryWorkStartDate = db.Column("WorkHistoryWorkStartDate",db.DateTime)
	WorkHistoryWorkEndDate = db.Column("WorkHistoryWorkEndDate",db.DateTime)
	WorkHistoryWorkEndReason = db.Column("WorkHistoryWorkEndReason",db.String(500))

	def to_json(self):
		json_data = {
			"workHistId": self.WorkHistId,
			"empId": self.EmpId,
			"whWorkPlace": self.WorkHistoryWorkPlace,
			"whWorkDesc": self.WorkHistoryWorkDesc,
			"whWorkDept": self.WorkHistoryWorkDept,
			"whWorkPos": self.WorkHistoryWorkPos,
			"whWorkStartDate": self.WorkHistoryWorkStartDate,
			"whWorkEndDate": self.WorkHistoryWorkEndDate,
			"whWorkEndReason": self.WorkHistoryWorkEndReason,
		}
		return json_data