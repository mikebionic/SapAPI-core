from main_pack.models.hr_department.models import (Employee,Award,Contract_type,Edu_level,
	Emp_status,Nationality,Profession,Rel_status,Relatives,School,School_type,
	Visited_countries,Work_history)

from main_pack.models.base.models import (Acc_type,Accounting_info,AdditionalInf1,AdditionalInf2,
	AdditionalInf3,AdditionalInf4,AdditionalInf5,AdditionalInf6,Bank,City,Company,Contact,Contact_type,
	Country,Currency,Db_inf,Department,Department_detail,Division,Gender,Image,Location,Password,
	Password_type,Language,Prog_language,Reg_num,Reg_num_type,Report_file,Rp_acc,Rp_acc_price_list,Warehouse)

from main_pack.models.commerce.models import (Barcode,Brand,Color,Res_color,Res_size,Res_translations,
	Res_unit,Size,Size_type,Unit,Usage_status,Resource,Res_category,
	Res_maker,Res_type)

from main_pack.models.base.models import (Company,Department,Department_detail,Division)

from main_pack.models.commerce.models import Color,Size

from main_pack.models.users.models import Users
from main_pack.models.base.models import Rp_acc,Reg_num

from main_pack import db, create_app

app = create_app()
app.app_context().push()

# db.drop_all()
# db.create_all()

#######  initial company migration ########
# comp = Company(CName="company")
# db.session.add(comp)
# div = Division(DivisionName="division",CId=1)
# db.session.add(div)
# dep = Department(DeptName="department")
# db.session.add(dep)
##########################

lastUser = Users.query.order_by(UId.desc()).first()
lastRpAcc = Rp_acc.query.order_by(RpAccId.desc()).first()
newUId = lastUser+1
newRpAccId = lastRpAcc+1
email = "muhammedjepbarov@gmail.com"
# # UPass is "123" hashed
password = "$2b$12$ZltRSL4D1LpcJuoFEzW7PO/rEio8LKxhK9vPEG3Jv7Zg9S07f4Q1G"

user = Users(UId=newUId,UName="administrator",UEmail=email,
	UPass=password,UShortName="AR",UFullName="Mike Bionic",UTypeId=1,RpAccId=newRpAccId)
db.session.add(user)

rp_acc = Rp_acc(RpAccId=newRpAccId,RpAccName="Mike Bionic",
	RpAccEMail=email,RpAccRegNo="ARAK1",RpAccTypeId=1,UId=newUId)
db.session.add(rp_acc)

regNum = Reg_num(UId=newUId,RegNumTypeId=6,
			RegNumPrefix="AK",RegNumLastNum=0)
db.session.add(regNum)

####### color migrate #########
color = Color(ColorName="Red",ColorCode="#e74c3c")
db.session.add(color)
color = Color(ColorName="Blue",ColorCode="#3498db")
db.session.add(color)
color = Color(ColorName="Green",ColorCode="#2ecc71")
db.session.add(color)
color = Color(ColorName="DarkBlue",ColorCode="#34495e")
db.session.add(color)
color = Color(ColorName="Yellow",ColorCode="#f1c40f")
db.session.add(color)
color = Color(ColorName="Orange",ColorCode="#e67e22")
db.session.add(color)
##################

###### sizes migrate ##########
size = Size(SizeName="S")
db.session.add(size)
size = Size(SizeName="M")
db.session.add(size)
size = Size(SizeName="L")
db.session.add(size)
size = Size(SizeName="XL")
db.session.add(size)
size = Size(SizeName="XXL")
db.session.add(size)
#########################

# db.session.commit()