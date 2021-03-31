
class Rel_status(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_rel_status"
	RelStatId = db.Column("RelStatId",db.Integer,nullable=False,primary_key=True)
	RelStatName_tkTM = db.Column("RelStatName_tkTM",db.String(50))#,nullable=False)
	RelStatDesc_tkTM = db.Column("RelStatDesc_tkTM",db.String(500))
	RelStatName_ruRU = db.Column("RelStatName_ruRU",db.String(50))#,nullable=False)
	RelStatDesc_ruRU = db.Column("RelStatDesc_ruRU",db.String(500))
	RelStatName_enUS = db.Column("RelStatName_enUS",db.String(50))#,nullable=False)
	RelStatDesc_enUS = db.Column("RelStatDesc_enUS",db.String(500))
	Relatives = db.relationship("Relatives",backref='rel_status',lazy=True)

	def to_json(self):
		json_data = {
			"RelStatId": self.RelStatId,
			"RelStatName_tkTM": self.RelStatName_tkTM,
			"RelStatDesc_tkTM": self.RelStatDesc_tkTM,
			"RelStatName_ruRU": self.RelStatName_ruRU,
			"RelStatDesc_ruRU": self.RelStatDesc_ruRU,
			"RelStatName_enUS": self.RelStatName_enUS,
			"RelStatDesc_enUS": self.RelStatDesc_enUS
		}
		return json_data