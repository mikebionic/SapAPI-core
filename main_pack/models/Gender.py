from main_pack import db


class Gender(db.Model):
	__tablename__ = "tbl_dk_gender"
	GenderId = db.Column("GenderId",db.Integer,nullable=False,primary_key=True)
	GenderName_tkTM = db.Column("GenderName_tkTM",db.String(100))
	GenderName_ruRU = db.Column("GenderName_ruRU",db.String(100))
	GenderName_enUS = db.Column("GenderName_enUS",db.String(100))
	Employee = db.relationship("Employee",backref='gender',lazy=True)
	Relatives = db.relationship("Relatives",backref='gender',lazy=True)
	Rp_acc = db.relationship("Rp_acc",backref='gender',lazy=True)
	Representative = db.relationship("Representative",backref='gender',lazy=True)

	def to_json_api(self):
		data = {
			"GenderId": self.GenderId,
			"GenderName_tkTM": self.GenderName_tkTM,
			"GenderName_ruRU": self.GenderName_ruRU,
			"GenderName_enUS": self.GenderName_enUS
		}
		return data