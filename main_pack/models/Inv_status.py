from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import BaseModel


class Inv_status(BaseModel, db.Model):
	__tablename__ = "tbl_dk_inv_status"
	InvStatId = db.Column("InvStatId",db.Integer,nullable=False,primary_key=True)
	InvStatGuid = db.Column("InvStatGuid",UUID(as_uuid=True),unique=True)
	InvStatName_tkTM = db.Column("InvStatName_tkTM",db.String(100),nullable=False)
	InvStatDesc_tkTM = db.Column("InvStatDesc_tkTM",db.String(500))
	InvStatName_ruRU = db.Column("InvStatName_ruRU",db.String(100))
	InvStatDesc_ruRU = db.Column("InvStatDesc_ruRU",db.String(500))
	InvStatName_enUS = db.Column("InvStatName_enUS",db.String(100))
	InvStatDesc_enUS = db.Column("InvStatDesc_enUS",db.String(500))
	Order_inv = db.relationship("Order_inv",backref='inv_status',lazy=True)
	Invoice = db.relationship("Invoice",backref='inv_status',lazy=True)
	Wh_invoice = db.relationship("Wh_invoice",backref='inv_status',lazy=True)

	def to_json_api(self):
		data = {
			"InvStatId": self.InvStatId,
			"InvStatGuid": self.InvStatGuid,
			"InvStatName_tkTM": self.InvStatName_tkTM,
			"InvStatDesc_tkTM": self.InvStatDesc_tkTM,
			"InvStatName_ruRU": self.InvStatName_ruRU,
			"InvStatDesc_ruRU": self.InvStatDesc_ruRU,
			"InvStatName_enUS": self.InvStatName_enUS,
			"InvStatDesc_enUS": self.InvStatDesc_enUS
		}

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data
	
	def get_all(
		id = None,
		uuid = None,
		name = None,
		name_tk = None,
		name_ru = None,
		name_en = None,
	):
		filtering = {"GCRecord": None}
		if id:
			filtering["InvStatId"] = id,

		db_query = Inv_status.query.filter_by(**filtering)
		
		if uuid:
			db_query = db_query.filter(Inv_status.InvStatGuid.ilike(uuid))
		if name:
			db_query = db_query.filter(Inv_status.InvStatName_tkTM.ilike(name))
		if name_tk:
			db_query = db_query.filter(Inv_status.InvStatName_tkTM.ilike(name_tk))
		if name_ru:
			db_query = db_query.filter(Inv_status.InvStatName_ruRU.ilike(name_ru))
		if name_en:
			db_query = db_query.filter(Inv_status.InvStatName_enUS.ilike(name_en))
		
		return db_query.all()