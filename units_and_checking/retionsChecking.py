from flask import Flask,session,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkk.db'
db = SQLAlchemy(app)


class Res_price_group(db.Model):
	__tablename__="tbl_dk_res_price_group"
	ResPriceGroupId = db.Column(db.Integer,nullable=False,primary_key=True)
	UsageStatusId = db.Column(db.Integer)
	ResPriceGroupName = db.Column(db.String(100),nullable=False)
	ResPriceGroupDesc = db.Column(db.String(500))
	ResPriceGroupAMEnabled = db.Column(db.Boolean,default=False)
	FromResPriceTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ToResPriceTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_res_price_type.ResPriceTypeId"))
	ResPriceGroupAMPerc = db.Column(db.Float,default=0)
	RoundingType = db.Column(db.Integer,default=1)

class Res_price_type(db.Model):
	__tablename__="tbl_dk_res_price_type"
	ResPriceTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	ResPriceTypeName_tkTM = db.Column(db.String(100),nullable=False)
	ResPriceTypeDesc_tkTM = db.Column(db.String(500))
	ResPriceTypeName_ruRU = db.Column(db.String(100))
	ResPriceTypeDesc_ruRU = db.Column(db.String(500))
	ResPriceTypeName_enUS = db.Column(db.String(100))
	ResPriceTypeDesc_enUS = db.Column(db.String(500))
	# Res_price = db.relationship('Res_price',backref='res_price_type',lazy=True)
	# multiple relationship
	Res_price_group = db.relationship('Res_price_group',foreign_keys='Res_price_group.FromResPriceTypeId',backref='res_price_type',lazy=True)
	Res_price_group = db.relationship('Res_price_group',foreign_keys='Res_price_group.ToResPriceTypeId',backref='res_price_type',lazy=True)
	# FromResPriceType = db.relationship('Res_price_group',foreign_keys=[FromResPriceTypeId],backref='res_price_type',lazy=True)
	# ToResPriceType = db.relationship('Res_price_group',foreign_keys=[ToResPriceTypeId],backref='res_price_type',lazy=True)
	
	# Res_price = db.relationship('Res_price',backref='res_price_type',lazy=True)

db.drop_all()
db.create_all()

price_type = Res_price_type(ResPriceTypeName_tkTM="planPrice")
db.session.add(price_type)
price_group = Res_price_group(ResPriceGroupName="newGroup",ToResPriceTypeId=1)
db.session.add(price_group)
db.session.commit()

if __name__ == "__main__":
	app.run(host="0.0.0.0" , port=5000, debug=True)
