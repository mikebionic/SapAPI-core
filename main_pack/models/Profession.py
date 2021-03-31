
class Profession(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_profession"
	ProfessionId = db.Column("ProfessionId",db.Integer,nullable=False,primary_key=True)
	ProfessionName_tkTM = db.Column("ProfessionName_tkTM",db.String(50))#,nullable=False)
	ProfessionDesc_tkTM = db.Column("ProfessionDesc_tkTM",db.String(500))
	ProfessionName_ruRU = db.Column("ProfessionName_ruRU",db.String(50))#,nullable=False)
	ProfessionDesc_ruRU = db.Column("ProfessionDesc_ruRU",db.String(500))
	ProfessionName_enUS = db.Column("ProfessionName_enUS",db.String(50))#,nullable=False)
	ProfessionDesc_enUS = db.Column("ProfessionDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='profession',lazy=True)

	def to_json(self):
		json_data = {
			"ProfessionId": self.ProfessionId,
			"ProfessionName_tkTM": self.ProfessionName_tkTM,
			"ProfessionDesc_tkTM": self.ProfessionDesc_tkTM,
			"ProfessionName_ruRU": self.ProfessionName_ruRU,
			"ProfessionDesc_ruRU": self.ProfessionDesc_ruRU,
			"ProfessionName_enUS": self.ProfessionName_enUS,
			"ProfessionDesc_enUS": self.ProfessionDesc_enUS
		}
		return json_data