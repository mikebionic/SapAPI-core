

class School_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_school_type"
	SchoolTypeId = db.Column("SchoolTypeId",db.Integer,nullable=False,primary_key=True)
	SchoolTypeName_tkTM = db.Column("SchoolTypeName_tkTM",db.String(50))
	SchoolTypeDesc_tkTM = db.Column("SchoolTypeDesc_tkTM",db.String(500))
	SchoolTypeName_ruRU = db.Column("SchoolTypeName_ruRU",db.String(50))
	SchoolTypeDesc_ruRU = db.Column("SchoolTypeDesc_ruRU",db.String(500))
	SchoolTypeName_enUS = db.Column("SchoolTypeName_enUS",db.String(50))
	SchoolTypeDesc_enUS = db.Column("SchoolTypeDesc_enUS",db.String(500))	
