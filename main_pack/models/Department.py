
class Department(AddInf, BaseModel, db.Model):
	__tablename__ = "tbl_dk_department"
	DeptId = db.Column("DeptId",db.Integer,nullable=False,primary_key=True)
	DeptName = db.Column("DeptName",db.String(100),nullable=False)
	DeptDesc = db.Column("DeptDesc",db.String(500))
	Employee = db.relationship("Employee",backref='department',lazy=True)
	Department_detail = db.relationship("Department_detail",backref='department',lazy=True)

