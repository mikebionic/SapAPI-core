
class Contact_type(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_contact_type"
	ContTypeId = db.Column("ContTypeId",db.Integer,nullable=False,primary_key=True)
	ContTypeName_tkTM = db.Column("ContTypeName_tkTM",db.String(100))
	ContTypeDesc_tkTM = db.Column("ContTypeDesc_tkTM",db.String(500))
	ContTypeName_ruRU = db.Column("ContTypeName_ruRU",db.String(100))
	ContTypeDesc_ruRU = db.Column("ContTypeDesc_ruRU",db.String(500))
	ContTypeName_enUS = db.Column("ContTypeName_enUS",db.String(100))
	ContTypeDesc_enUS = db.Column("ContTypeDesc_enUS",db.String(500))
	Contact = db.relationship("Contact",backref='contact_type',lazy=True)

	def to_json(self):
		json_data = {
			"ContactTypeId": self.ContactTypeId,
			"ContactTypeName_tkTM": self.ContactTypeName_tkTM,
			"ContactTypeDesc_tkTM": self.ContactTypeDesc_tkTM,
			"ContactTypeName_ruRU": self.ContactTypeName_ruRU,
			"ContactTypeDesc_ruRU": self.ContactTypeDesc_ruRU,
			"ContactTypeName_enUS": self.ContactTypeName_enUS,
			"ContactTypeDesc_enUS": self.ContactTypeDesc_enUS,
			"CreatedDate": apiDataFormat(self.CreatedDate),
			"ModifiedDate": apiDataFormat(self.ModifiedDate),
			"SyncDateTime": apiDataFormat(self.SyncDateTime),
			"CreatedUId": self.CreatedUId,
			"ModifiedUId": self.ModifiedUId,
			"GCRecord": self.GCRecord
		}
		return json_data