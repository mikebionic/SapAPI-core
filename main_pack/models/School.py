from main_pack import db
from main_pack.models import AddInf, BaseModel


class School(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_school"
	SchoolId = db.Column("SchoolId",db.Integer,nullable=False,primary_key=True)
	EmpId = db.Column("EmpId",db.Integer,db.ForeignKey("tbl_dk_employee.EmpId"))
	SchoolTypeId = db.Column("SchoolTypeId",db.Integer,db.ForeignKey("tbl_dk_school_type.SchoolTypeId"))
	SchoolName = db.Column("SchoolName",db.String(255),nullable=False)
	SchoolDesc = db.Column("SchoolDesc",db.String(500))
	SchoolPlace = db.Column("SchoolPlace",db.String(255))
	SchoolEduStartDate = db.Column("SchoolEduStartDate",db.DateTime)
	SchoolEduEndDate = db.Column("SchoolEduEndDate",db.DateTime)
	SchoolProfession = db.Column("SchoolProfession",db.String(255))
	SchoolIsGraduated = db.Column("SchoolIsGraduated",db.Boolean,default=False)

	def to_json_api(self):
		data = {
			"schoolId": self.SchoolId,
			"empId": self.EmpId,
			"schoolType": self.SchoolTypeId,
			"schoolName": self.SchoolName,
			"schoolDesc": self.SchoolDesc,
			"schoolPlace": self.SchoolPlace,
			"eduStartDate": self.SchoolEduStartDate,
			"eduEndDate": self.SchoolEduEndDate,
			"schoolProfession": self.SchoolProfession,
			"isGraduated": self.SchoolIsGraduated
		}

		for key, value in AddInf.to_json_api(self).items():
			data[key] = value

		for key, value in BaseModel.to_json_api(self).items():
			data[key] = value

		return data
