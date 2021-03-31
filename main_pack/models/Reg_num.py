
class Reg_num(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_reg_num"
	RegNumId = db.Column("RegNumId",db.Integer,nullable=False,primary_key=True)
	RegNumTypeId = db.Column("RegNumTypeId",db.Integer,db.ForeignKey("tbl_dk_reg_num_type.RegNumTypeId"))
	UId = db.Column("UId",db.Integer,db.ForeignKey("tbl_dk_users.UId"))
	RegNumPrefix = db.Column("RegNumPrefix",db.String(100))
	RegNumLastNum = db.Column("RegNumLastNum",db.Integer,nullable=False)
	RegNumSuffix = db.Column("RegNumSuffix",db.String(100))

	def registerLastNum(self,RegNumLastNum):
		self.RegNumLastNum+=1