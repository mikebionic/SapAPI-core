from main_pack import db
from datetime import datetime
from flask_login import current_user

class Product(db.Model):
	__tablename__ = "tbl_me_products"
	ProductId = db.Column(db.Integer, nullable=False, primary_key=True)
	ProductRegId = db.Column(db.String)
	ProductSeller = db.Column(db.String)
	ProductTitle = db.Column(db.String)
	ProductDesc = db.Column(db.String)
	DateRegistered = db.Column(db.DateTime, default=datetime.utcnow)
	ProductPicture = db.Column(db.String)
	RegUId = db.Column(db.Integer)
	def get_id(self):
		return (self.ProductId)
	def __repr__(self):
		return "Document('{}','{}','{}')".format(
			self.DocId,self.DocTitle,self.DateReceived)