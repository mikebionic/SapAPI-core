from main_pack.models.hr_department.models import (Employee,Award,Contract_type,Edu_level,
	Emp_status,Nationality,Profession,Rel_status,Relatives,School,School_type,
	Visited_countries,Work_history,db)

from main_pack.models.base.models import (Acc_type,Accounting_info,AdditionalInf1,AdditionalInf2,
	AdditionalInf3,AdditionalInf4,AdditionalInf5,AdditionalInf6,Bank,City,Company,Contact,Contact_type,
	Country,Currency,Db_inf,Department,Department_detail,Division,Gender,Image,Location,Password,
	Password_type,Prog_language,Reg_num,Reg_num_type,Report_file,Resource,Rp_acc,Warehouse,db)

from main_pack.models.users.models import Users
from main_pack.models.commerce.models import Product,db
from main_pack import db, create_app
app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()

# user = Users(UName="admin", EMail="admin@post.in", UFullName="Administrator",UPass="admin123", UType=1)
# db.session.add(user)

comp = Company(CName="company")
db.session.add(comp)
div = Division(DivisionName="division",CId=1)
db.session.add(div)
dep = Department(DeptName="department")
db.session.add(dep)

db.session.commit()

# types:
# 1 = admin
# 2 = just user