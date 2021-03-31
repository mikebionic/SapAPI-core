

class Password_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_password_type"
	PsswTypeId = db.Column("PsswTypeId",db.Integer,nullable=False,primary_key=True)
	PsswTypeName = db.Column("PsswTypeName",db.String(100),nullable=False)
	PsswTypeDesc = db.Column("PsswTypeDesc",db.String(500))
	Password = db.relationship("Password",backref='password_type',lazy=True)

