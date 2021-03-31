
class Nationality(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_nationality"
	NatId = db.Column("NatId",db.Integer,nullable=False,primary_key=True)
	NatName_tkTM = db.Column("NatName_tkTM",db.String(50))#,nullable=False)
	NatDesc_tkTM = db.Column("NatDesc_tkTM",db.String(500))
	NatName_ruRU = db.Column("NatName_ruRU",db.String(50))#,nullable=False)
	NatDesc_ruRU = db.Column("NatDesc_ruRU",db.String(500))
	NatName_enUS = db.Column("NatName_enUS",db.String(50))#,nullable=False)
	NatDesc_enUS = db.Column("NatDesc_enUS",db.String(500))
	Employee = db.relationship("Employee",backref='nationality',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='nationality',lazy=True)

	def to_json_api(self):
		json_data = {
			"NatId": self.NatId,
			"NatName_tkTM": self.NatName_tkTM,
			"NatDesc_tkTM": self.NatDesc_tkTM,
			"NatName_ruRU": self.NatName_ruRU,
			"NatDesc_ruRU": self.NatDesc_ruRU,
			"NatName_enUS": self.NatName_enUS,
			"NatDesc_enUS": self.NatDesc_enUS
		}
		return json_data