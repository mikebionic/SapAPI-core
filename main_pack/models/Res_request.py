from sqlalchemy.dialects.postgresql import UUID

from main_pack import db
from main_pack.models import AddInf, BaseModel

class Res_request(AddInf,BaseModel, db.Model):
	__tablename__ = "tbl_dk_res_request"
	ResReqId = db.Column("ResReqId",db.Integer,nullable=False,primary_key=True)
	ResReqGuid = db.Column("ResReqGuid", UUID(as_uuid=True),unique=True)
	RpAccId = db.Column("RpAccId",db.Integer, db.ForeignKey("tbl_dk_rp_acc.RpAccId"))
	ResponsibleUid = db.Column("ResponsibleUid",db.Integer, db.ForeignKey("tbl_dk_users.UId"))
	ResReqName = db.Column("ResReqName", db.String(100), nullable=False)
	ResReqDesc = db.Column("ResReqDesc", db.String(500))
	ResReqImageUrl = db.Column("ResReqImageUrl", db.String(255))
	ResReqIsVisible = db.Column("ResReqIsVisible", db.Boolean, default=False)
	ClientName = db.Column("ClientName", db.String(100), nullable=False)
	ClientEmail = db.Column("ClientEmail", db.String(100), nullable=False)
	ClientPhoneNumber = db.Column("ClientPhoneNumber", db.String(100), nullable=False)

	def to_json_api(self):
		data = {
			"ResReqId": self.ResReqId,
			"ResReqGuid": self.ResReqGuid,
			"RpAccId": self.RpAccId,
			"ResponsibleUid": self.ResponsibleUid,
			"ResReqName": self.ResReqName,
			"ResReqDescription": self.ResReqDesc,
			"ResReqImageUrl": self.ResReqImageUrl,
			"ResReqIsVisible": self.ResReqIsVisible,
			"ClientName": self.ClientName,
			"ClientEmail": self.ClientEmail,
			"ClientPhoneNumber": self.ClientPhoneNumber

		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data