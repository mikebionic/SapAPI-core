
class Relatives(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_relatives"
	RelId = db.Column("RelId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RelStatId = db.Column("RelStatId",db.Integer,db.ForeignKey("tbl_dk_rel_status.RelStatId"))
	RelPersonName = db.Column("RelPersonName",db.String(100),nullable=False)
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	RelBirthDate = db.Column("RelBirthDate",db.DateTime)
	RelBirthPlace = db.Column("RelBirthPlace",db.String(255))
	RelWorkPlace = db.Column("RelWorkPlace",db.String(255))
	RelWorkPosition = db.Column("RelWorkPosition",db.String(255))
	RelResidence = db.Column("RelResidence",db.String(255))

	def to_json(self):
		json_data = {
			"relativesId": self.RelId,
			"empId": self.EmpId,
			"relativesStatus": self.RelStatId,
			"relativesName": self.RelPersonName,
			"relativesGender": self.GenderId,
			"relativesBirthDate": self.RelBirthDate,
			"relativesBirthPlace": self.RelBirthPlace,
			"relativesWorkPlace": self.RelWorkPlace,
			"relativesWorkPosition": self.RelWorkPosition,
			"relativesResidence": self.RelResidence
		}
		return json_data

