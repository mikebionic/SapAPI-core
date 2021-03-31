from main_pack import db
from main_pack.models import BaseModel


class Rp_acc_status(BaseModel, db.Model):
	__tablename__ = "tbl_dk_rp_acc_status"
	RpAccStatusId = db.Column("RpAccStatusId",db.Integer,nullable=False,primary_key=True)
	RpAccStatusName_tkTM = db.Column("RpAccStatusName_tkTM",db.String(100),nullable=False)
	RpAccStatusDesc_tkTM = db.Column("RpAccStatusDesc_tkTM",db.String(500))
	RpAccStatusName_ruRU = db.Column("RpAccStatusName_ruRU",db.String(100))
	RpAccStatusDesc_ruRU = db.Column("RpAccStatusDesc_ruRU",db.String(500))
	RpAccStatusName_enUS = db.Column("RpAccStatusName_enUS",db.String(100))
	RpAccStatusdesc_enUS = db.Column("RpAccStatusdesc_enUS",db.String(500))
	Rp_acc = db.relationship("Rp_acc",backref='rp_acc_status',lazy=True)

	def to_json(self):
		data = {
			"RpAccStatusId": self.RpAccStatusId,
			"RpAccStatusName_tkTM": self.RpAccStatusName_tkTM,
			"RpAccStatusDesc_tkTM": self.RpAccStatusDesc_tkTM,
			"RpAccStatusName_ruRU": self.RpAccStatusName_ruRU,
			"RpAccStatusDesc_ruRU": self.RpAccStatusDesc_ruRU,
			"RpAccStatusName_enUS": self.RpAccStatusName_enUS,
			"RpAccStatusdesc_enUS": self.RpAccStatusdesc_enUS
		}

		for key, value in BaseModel.to_json(self).items():
			data[key] = value

		return data
