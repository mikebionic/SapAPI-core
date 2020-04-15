from main_pack import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# from main_pack.models.hr_department.models import (Employee,Award,Contract_type,Edu_level,
# 	Emp_status,Nationality,Profession,Rel_status,Relatives,School,School_type,
# 	Visited_countries,Work_history,db)

# from main_pack.models.base.models import (Acc_type,Accounting_info,AdditionalInf1,AdditionalInf2,
# 	AdditionalInf3,AdditionalInf4,AdditionalInf5,AdditionalInf6,Bank,City,Company,Contact,Contact_type,
# 	Country,Currency,Db_inf,Department,Department_detail,Division,Gender,Image,Location,Password,
# 	Password_type,Prog_language,Reg_num,Reg_num_type,Report_file,Resource,Rp_acc,Warehouse,db)


from main_pack.models.base.models import CreatedModifiedInfo, AddInf

class CreatedModifiedInfo(object):
	CreatedDate = db.Column(db.DateTime,default=datetime.now)
	ModifiedDate = db.Column(db.DateTime,default=datetime.now)
	CreatedUId = db.Column(db.Integer)
	ModifiedUId = db.Column(db.Integer)
	GCRecord = db.Column(db.Integer)

	def createdInfo(self,UId):
		self.CreatedUId = UId

	def modifiedInfo(self,UId):
		self.ModifiedDate = datetime.now()
		self.ModifiedUId = UId

class AddInf(object):
	AddInf1 = db.Column(db.String(500))
	AddInf2 = db.Column(db.String(500))
	AddInf3 = db.Column(db.String(500))
	AddInf4 = db.Column(db.String(500))
	AddInf5 = db.Column(db.String(500))
	AddInf6 = db.Column(db.String(500))


@login_manager.user_loader
def load_user(UId):
	return Users.query.get(int(UId))

class Users(AddInf,CreatedModifiedInfo,db.Model,UserMixin):
	__tablename__="tbl_dk_users"
	UId = db.Column(db.Integer,nullable=False,primary_key=True)
	CId = db.Column(db.Integer,db.ForeignKey("tbl_dk_company.CId"))
	DivisionId = db.Column(db.Integer,db.ForeignKey("tbl_dk_division.DivisionId"))
	UFullName = db.Column(db.String(100),nullable=False)
	UName = db.Column(db.String(60),nullable=False)
	UEmail = db.Column(db.String(100),unique=True,nullable =False)
	UPass = db.Column(db.String(60))
	UShortName = db.Column(db.String(10))
	EmpId = db.Column(db.Integer)
	UTypeId = db.Column(db.Integer,db.ForeignKey("tbl_dk_user_type.UTypeId"))
	
	def get_id(self):
		return (self.UId)

	def get_reset_token(self,expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
		return s.dumps({'UId':self.UId}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			UId = s.loads(token)['UId']
		except:
			return None
		return	Users.query.get(UId)
	def __repr__ (self):
		return "Users('{}','{}')".format(self.UId,self.UName)

class User_type(CreatedModifiedInfo,db.Model):
	__tablename__="tbl_dk_user_type"
	UTypeId = db.Column(db.Integer,nullable=False,primary_key=True)
	UTypeName_tkTM = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_tkTM = db.Column(db.String(500))
	UTypeName_ruRU = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_ruRU = db.Column(db.String(500))
	UTypeName_enUS = db.Column(db.String(50))#,nullable=False)
	UTypeDesc_enUS = db.Column(db.String(500))
	Users = db.relationship('Users',backref='user_type',lazy=True)