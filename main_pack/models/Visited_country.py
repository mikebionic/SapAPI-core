class Visited_country(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_visited_countries"
	VCId = db.Column("VCId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	VCCountryName = db.Column("VCCountryName",db.String(50),nullable=False)
	VCCountryDesc = db.Column("VCCountryDesc",db.String(500))
	VCPurpose = db.Column("VCPurpose",db.String(500))
	VCStartDate = db.Column("VCStartDate",db.DateTime)
	VCEndDate = db.Column("VCEndDate",db.DateTime)

	def to_json_api(self):
		json_data = {
			"vcId": self.VCId,
			"empId": self.EmpId,
			"vcCountryName": self.VCCountryName,
			"vcCountryDesc": self.VCCountryDesc,
			"vcPurpose": self.VCPurpose,
			"vcStartDate": self.VCStartDate,
			"vcEndDate": self.VCEndDate
		}
		return json_data
