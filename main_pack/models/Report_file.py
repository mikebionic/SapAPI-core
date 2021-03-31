

class Report_file(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_report_file"
	RpFileId = db.Column("RpFileId",db.Integer,nullable=False,primary_key=True)
	RpFileTypeId = db.Column("RpFileTypeId",db.Integer,nullable=False,default=0)
	RpFileName = db.Column("RpFileName",db.String(100))
	RpFileDesc = db.Column("RpFileDesc",db.String(100))
	RpFileFileName = db.Column("RpFileFileName",db.String(100))
	RpIsDefault = db.Column("RpIsDefault",db.Boolean,default=False)