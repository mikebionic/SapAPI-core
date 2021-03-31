

class Location(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_location"
	LocId = db.Column("LocId",db.Integer,nullable=False,primary_key=True)
	CId = db.Column("CId",db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	BankId = db.Column("BankId",db.Integer,db.ForeignKey("tbl_dk_bank.BankId"))
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	RpAccId = db.Column("RpAccId",db.Integer,db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	CountryId = db.Column("CountryId",db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityId = db.Column("CityId",db.Integer,db.ForeignKey("tbl_dk_city.CityId"))
	LocAddress = db.Column("LocAddress",db.String(500),nullable=False)
	LocAddressOffical = db.Column("LocAddressOffical",db.String(500),nullable=False)
	LocAddressReal = db.Column("LocAddressReal",db.String(500),nullable=False)
	LocPostCode = db.Column("LocPostCode",db.String(25))
	LocLatitude = db.Column("LocLatitude",db.Integer)
	LocLongitude = db.Column("LocLongitude",db.Integer)
