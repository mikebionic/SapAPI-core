

class Db_inf(db.Model):
	__tablename__ = "tbl_dk_db_inf"
	DbInfId = db.Column("DbInfId",db.Integer,nullable=False,primary_key=True)
	DbInfDbVer = db.Column("DbInfDbVer",db.String(100),nullable=False)
	DbInfGuid = db.Column("DbInfGuid",UUID(as_uuid=True))
	GCRecord = db.Column("GCRecord",db.Integer)