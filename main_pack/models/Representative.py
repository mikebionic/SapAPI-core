
class Representative(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_representative"
	ReprId = db.Column("ReprId",db.Integer,nullable=False,primary_key=True)
	ReprStatusId = db.Column("ReprStatusId",db.Integer,nullable=False,default=1)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivId = db.Column("DivId",db.Integer,db.ForeignKey("tbl_dk_division.DivId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	GenderId = db.Column("GenderId",db.Integer,db.ForeignKey("tbl_dk_gender.GenderId"))
	ReprRegNo = db.Column("ReprRegNo",db.String(100),nullable=False)
	ReprName = db.Column("ReprName",db.String(100),nullable=False)
	ReprDesc = db.Column("ReprDesc",db.String(500))
	ReprProfession = db.Column("ReprProfession",db.String(100))
	ReprMobilePhoneNumber = db.Column("ReprMobilePhoneNumber",db.String(100))
	ReprHomePhoneNumber = db.Column("ReprHomePhoneNumber",db.String(100))
	ReprWorkPhoneNumber = db.Column("ReprWorkPhoneNumber",db.String(100))
	ReprWorkFaxNumber = db.Column("ReprWorkFaxNumber",db.String(100))
	ReprZipCode = db.Column("ReprZipCode",db.String(100))
	ReprEMail = db.Column("ReprEMail",db.String(100))
	CreatedDate = db.Column("CreatedDate",db.DateTime,default=datetime.now)
	ModifiedDate = db.Column("ModifiedDate",db.DateTime,default=datetime.now)
	CreatedUId = db.Column("CreatedUId",db.Integer,default=0)
	ModifiedUId = db.Column("ModifiedUId",db.Integer,default=0)
	MyProperty = db.Column("MyProperty",db.Integer)
	Rp_acc = db.relationship("Rp_acc",backref='representative',foreign_keys='Rp_acc.ReprId',lazy='joined')

	def to_json_api(self):
		json_data = {
			"ReprId": self.ReprId,
			"ReprStatusId": self.ReprStatusId,
			"CId": self.CId,
			"DivId": self.DivId,
			"RpAccId": self.RpAccId,
			"GenderId": self.GenderId,
			"ReprRegNo": self.ReprRegNo,
			"ReprName": self.ReprName,
			"ReprDesc": self.ReprDesc,
			"ReprProfession": self.ReprProfession,
			"ReprMobilePhoneNumber": self.ReprMobilePhoneNumber,
			"ReprHomePhoneNumber": self.ReprHomePhoneNumber,
			"ReprWorkPhoneNumber": self.ReprWorkPhoneNumber,
			"ReprWorkFaxNumber": self.ReprWorkFaxNumber,
			"ReprZipCode": self.ReprZipCode,
			"ReprEMail": self.ReprEMail,
			"CreatedDate": self.CreatedDate,
			"ModifiedDate": self.ModifiedDate,
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"MyProperty": self.MyProperty,
			"AddInf1": self.AddInf1,
			"AddInf2": self.AddInf2,
			"AddInf3": self.AddInf3,
			"AddInf4": self.AddInf4,
			"AddInf5": self.AddInf5,
			"AddInf6": self.AddInf6,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data