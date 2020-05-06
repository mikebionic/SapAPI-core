# from main_pack.models.hr_department.models import (Employee,Award,Contract_type,Edu_level,
# 	Emp_status,Nationality,Profession,Rel_status,Relatives,School,School_type,
# 	Visited_countries,Work_history)

# from main_pack.models.base.models import (Acc_type,Accounting_info,AdditionalInf1,AdditionalInf2,
# 	AdditionalInf3,AdditionalInf4,AdditionalInf5,AdditionalInf6,Bank,City,Company,Contact,Contact_type,
# 	Country,Currency,Db_inf,Department,Department_detail,Division,Gender,Image,Location,Password,
# 	Password_type,Language,Prog_language,Reg_num,Reg_num_type,Report_file,Resource,Res_category,
# 	Resource_maker,Resource_type,Rp_acc,Rp_acc_price_list,Warehouse)

# from main_pack.models.commerce.models import (Barcode,Brand,Color,Res_color,Res_size,Res_translations,
# 	Res_unit,Size,Size_type,Unit,Usage_status)

from main_pack.models.base.models import (Company,Department,Department_detail,Division)


from main_pack.models.users.models import Users

from main_pack import db, create_app

app = create_app()
app.app_context().push()

# db.drop_all()
# db.create_all()

comp = Company(CName="company")
db.session.add(comp)
div = Division(DivisionName="division",CId=1)
db.session.add(div)
dep = Department(DeptName="department")
db.session.add(dep)

# user = Users(UName="mike",UEmail="muhammedjepbarov@gmail.com",UPass="")

db.session.commit()