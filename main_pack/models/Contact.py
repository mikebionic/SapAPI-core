

class Contact(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_contact"
	ContId = db.Column("ContId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	BankId = db.Column("BankId",db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	ContTypeId = db.Column("ContTypeId",db.Integer,db.ForeignKey("tbl_dk_contact_type.ContTypeId"))
	ContValue = db.Column("ContValue",db.String(200),nullable=False)
	ContDesc = db.Column("ContDesc",db.String(500))