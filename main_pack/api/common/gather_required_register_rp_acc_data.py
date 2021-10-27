from datetime import datetime
import uuid

from main_pack.key_generator.utils import makeRegNo, generate
from main_pack import db
from main_pack.config import Config
from main_pack.models import (
	User,
	Company,
	Division,
)


def gather_required_register_rp_acc_data():
	UId, CId, DivId, RpAccRegNo, RpAccGuid = None, None, None, '', uuid.uuid4()

	main_user = User.query\
		.filter_by(GCRecord = None, UTypeId = 1)\
		.first()
	UId = main_user.UId

	try:
		reg_num = generate(UId=UId, RegNumTypeName='rp_code')
		RpAccRegNo = makeRegNo(main_user.UShortName, reg_num.RegNumPrefix, reg_num.RegNumLastNum + 1, '',RegNumTypeName='rp_code')
		reg_num.RegNumLastNum = reg_num.RegNumLastNum + 1
		db.session.commit()
	except Exception as ex:
		print(f"{datetime.now()} | UI Register Reg Num generation Exception: {ex}")
		RpAccRegNo = str(datetime.now().timestamp())
		# flash(lazy_gettext('Error generating Registration number'),'warning')
		# return redirect(url_for('commerce_auth.register'))

	company = Company.query.filter_by(CGuid = Config.MAIN_CGUID).first()
	if not company:
		company = Company.query.first()

	division = Division.query.filter_by(DivGuid = Config.C_REGISTRATION_DIVGUID).first()
	if not division:
		division = Division.query.first()

	CId = company.CId if company else None
	DivId = division.DivId if division else None

	return UId, CId, DivId, RpAccRegNo, RpAccGuid


