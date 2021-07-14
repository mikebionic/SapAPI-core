# -*- coding: utf-8 -*-
from main_pack.models import Barcode

def collect_barcode_data(
	BarcodeId = None,
	BarcodeGuid = None,
	CId = None,
	DivId = None,
	ResId = None,
	UnitId = None,
	BarcodeVal = None,
):

	filtering = {"GCRecord": None}

	if BarcodeId:
		filtering["BarcodeId"] = BarcodeId

	if BarcodeGuid:
		filtering["BarcodeGuid"] = BarcodeGuid

	if CId:
		filtering["CId"] = CId

	if DivId:
		filtering["DivId"] = DivId

	if ResId:
		filtering["ResId"] = ResId

	if UnitId:
		filtering["UnitId"] = UnitId

	db_barcodes = Barcode.query.filter_by(**filtering)


	if BarcodeVal:
		db_barcodes = db_barcodes.filter(Barcode.BarcodeVal.ilike(f"%{BarcodeVal}%"))



	db_barcodes = db_barcodes.all()

	data = [barcode_data.to_json_api() for barcode_data in db_barcodes]

	return data