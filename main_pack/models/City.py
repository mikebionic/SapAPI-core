
class City(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_city"
	CityId = db.Column("CityId",db.Integer,nullable=False,primary_key=True)
	CountryId = db.Column("CountryId",db.Integer,db.ForeignKey("tbl_dk_country.CountryId"))
	CityName = db.Column("CityName",db.String(50),nullable=False)
	CityDesc = db.Column("CityDesc",db.String(500))
	Location = db.relationship("Location",backref='city',lazy=True)