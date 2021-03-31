

class Password(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_password"
	PsswId = db.Column("PsswId",db.Integer,nullable=False,primary_key=True)
	PsswUId = db.Column("PsswUId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	PsswTypeId = db.Column("PsswTypeId",db.Integer,db.ForeignKey("tbl_dk_password_type.PsswTypeId"))
	PsswPassHash = db.Column("PsswPassHash",db.String(255))
	PsswPassword= db.Column("PsswPasswor",db.String(100),nullable=False)
