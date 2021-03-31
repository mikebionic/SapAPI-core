
class Prog_language(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_prog_language"
	LangId = db.Column("LangId",db.Integer,nullable=False,primary_key=True)
	LangName = db.Column("LangName",db.String(50),nullable=False)
	LangDesc = db.Column("LangDesc",db.String(200))