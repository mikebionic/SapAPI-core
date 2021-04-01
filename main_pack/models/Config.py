
class Config(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_config"
	CfId = db.Column("CfId",db.Integer,primary_key=True)
	MainCfId = db.Column("MainCfId",db.Integer)
	CfTypeId = db.Column("CfTypeId",db.Integer,db.ForeignKey("tbl_dk_config_type.CfTypeId"))
	CfGuid = db.Column("CfGuid",UUID(as_uuid=True))
	CfName = db.Column("CfName",db.String(100),nullable=False)
	CfDesc = db.Column("CfDesc",db.String(500))
	CfIntVal = db.Column("CfIntVal",db.Integer)
	CfStringVal = db.Column("CfStringVal",db.String(500))

	def to_json_api(self):
		json_data = {
			"CfId": self.CfId,
			"MainCfId": self.MainCfId,
			"CfTypeId": self.CfTypeId,
			"CfGuid": self.CfGuid,
			"CfName": self.CfName,
			"CfDesc": self.CfDesc,
			"CfIntVal": self.CfIntVal,
			"CfStringVal": self.CfStringVal,
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