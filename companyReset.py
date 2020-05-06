# from main_pack.models.base.models import (Contact)
from main_pack.models.base.models import Reg_num,Reg_num_type
# from main_pack.key_generator.utils import makeRegNum,generate,validate


from main_pack.models.base.models import Resource
# used foreign keys
from main_pack.models.commerce.models import Unit,Brand,Usage_status
from main_pack.models.base.models import Company,Division,Res_category,Resource_type,Resource_maker,Rp_acc
####
# used relationship
from main_pack.models.commerce.models import (Barcode,Res_color,Res_size,Res_translations,Unit,Res_unit,
	Inv_line,Inv_line_det,Order_inv_line,Res_price,Res_total,Res_trans_inv_line,Res_transaction,Rp_acc_resource,
	Sale_agr_res_price,Res_discount)
from main_pack.models.base.models import Image

from main_pack import db, create_app

app = create_app()
app.app_context().push()

# db.drop_all()
# db.create_all()