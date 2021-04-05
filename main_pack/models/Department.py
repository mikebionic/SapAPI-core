from main_pack import db
from main_pack.models import AddInf, BaseModel


class Department(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_department"
	DeptId = db.Column("DeptId",db.Integer,nullable=False,primary_key=True)
	DeptName = db.Column("DeptName",db.String(100),nullable=False)
	DeptDesc = db.Column("DeptDesc",db.String(500))
	Employee = db.relationship("Employee",backref='department',lazy=True)
	Department_detail = db.relationship("Department_detail",backref='department',lazy=True)

	def to_json_api(self):
		data = {
			"DeptId": self.DeptId,
			"DeptName": self.DeptName,
			"DeptDesc": self.DeptDesc
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data