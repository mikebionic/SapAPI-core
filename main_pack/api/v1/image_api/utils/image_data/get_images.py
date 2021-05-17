from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
import dateutil.parser
from sqlalchemy import and_, or_

from main_pack.models import Image


def get_images(
	DivId = None,
	notDivId = None,
	synchDateTime = None,
	UId = None,
	EmpId = None,
	BrandId = None,
	CId = None,
	RpAccId = None,
	ResId = None,
	ResCatId = None,
	ProdId = None,
	users = None,
	brands = None,
	resources = None,
	rp_accs = None,
	prods = None,
	employees = None,
	categories = None,
	companies = None,
	images_to_exclude = None,
):

	filtering = {"GCRecord": None}

	if UId:
		filtering["UId"] = UId
	if EmpId:
		filtering["EmpId"] = EmpId
	if BrandId:
		filtering["BrandId"] = BrandId
	if CId:
		filtering["CId"] = CId
	if RpAccId:
		filtering["RpAccId"] = RpAccId
	if ResId:
		filtering["ResId"] = ResId
	if ResCatId:
		filtering["ResCatId"] = ResCatId
	if ProdId:
		filtering["ProdId"] = ProdId

	images = Image.query.filter_by(**filtering)

	if DivId:
		images = images\
			.join(Resource, and_(
				Resource.ResId == Image.ResId,
				Resource.DivId == DivId))
	if notDivId:
		images = images\
			.join(Resource, and_(
				Resource.ResId == Image.ResId,
				Resource.DivId != notDivId))

	if synchDateTime:
		if (type(synchDateTime) != datetime):
			synchDateTime = dateutil.parser.parse(synchDateTime)
		images = images.filter(Image.ModifiedDate > (synchDateTime - timedelta(minutes = 5)))


	if images_to_exclude:
		try:
			filenames_to_exclude = [img["FileName"] for img in images_to_exclude]
			guids_to_exclude = [img["ImgGuid"] for img in images_to_exclude]

			# # faseter method but not validating both, validates separate..
			# images = images.filter(Image.FileName.notin_(filenames_to_exclude) and Image.ImgGuid.notin_(guids_to_exclude))

			# # I do an each filtering for guid filename info to validate both values
			for filename in filenames_to_exclude:
				order = filenames_to_exclude.index(filename)
				image_guid = guids_to_exclude[order]
				images = images.filter(Image.FileName != filename and Image.ImgGuid != image_guid)

		except:
			pass

	if (resources or brands or rp_accs or categories or users or employees or companies or prods):
		images = images.filter(
			or_(
				Image.ResId != None if resources else Image.ResId == 0,
				Image.RpAccId != None if rp_accs else Image.RpAccId == 0,
				Image.BrandId != None if brands else Image.BrandId == 0,
				Image.ResCatId != None if categories else Image.ResCatId == 0,
				Image.EmpId != None if employees else Image.EmpId == 0,
				Image.UId != None if users else Image.UId == 0,
				Image.CId != None if companies else Image.CId == 0,
				Image.ProdId != None if prods else Image.ProdId == 0,
			))

	images = images.options(
		joinedload(Image.resource),
		joinedload(Image.rp_acc))\
	.all()

	data = []
	for image in images:
		image_info = image.to_json_api()
		image_info["ResRegNo"] = image.resource.ResRegNo if image.resource and not image.resource.GCRecord else None
		image_info["ResGuid"] = image.resource.ResGuid if image.resource and not image.resource.GCRecord else None
		image_info["RpAccGuid"] = image.rp_acc.RpAccGuid if image.rp_acc and not image.rp_acc.GCRecord else None
		data.append(image_info)

	return data
