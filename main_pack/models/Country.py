

class Country(AddInf,CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_country"
	CountryId = db.Column("CountryId",db.Integer,nullable=False,primary_key=True)
	CountryName = db.Column("CountryName",db.String(50),nullable=False)
	CountryDesc = db.Column("CountryDesc",db.String(500))
	City = db.relationship("City",backref='country',lazy=True)
	Location = db.relationship("Location",backref='country',lazy=True)
