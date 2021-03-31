
class Res_unit(CreatedModifiedInfo,db.Model):
	__tablename__ = "tbl_dk_res_unit"
	ResUnitId = db.Column("ResUnitId",db.Integer,nullable=False,primary_key=True)
	ResId = db.Column("ResId",db.Integer,db.ForeignKey("tbl_dk_resource.ResId"))
	ResUnitUnitId = db.Column("ResUnitUnitId",db.Integer,db.ForeignKey("tbl_dk_unit.UnitId"))
	ResUnitConvAmount = db.Column("ResUnitConvAmount",db.Float,nullable=False)
	ResUnitConvTypeId = db.Column("ResUnitConvTypeId",db.Integer,nullable=False)

	def to_json_api(self):
		json_data = {
			"ResUnitId": self.ResUnitId,
			"ResId": self.ResId,
			"ResUnitUnitId": self.ResUnitUnitId,
			"ResUnitConvAmount": self.ResUnitConvAmount,
			"ResUnitConvTypeId": self.ResUnitConvTypeId
		}
		return json_data