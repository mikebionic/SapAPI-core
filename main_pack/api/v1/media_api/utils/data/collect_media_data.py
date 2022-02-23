# -*- coding: utf-8 -*-
from sqlalchemy import and_, extract
from sqlalchemy.orm import joinedload
from datetime import datetime
import dateutil.parser

from main_pack.models import Media, Language

def collect_media_data(
	MediaId = None,
	MediaTitle = None,
	MediaName = None,
	MediaBody = None,
	MediaAuthor = None,
	MediaIsFeatured = None,
	MediaCatId = None,
	LangName = None,
	startDate = None,
	endDate = datetime.now(),
):

	filtering = {"GCRecord": None}

	if MediaId:
		filtering["MediaId"] = MediaId

	if MediaIsFeatured:
		filtering["MediaIsFeatured"] = True
	if MediaCatId:
		filtering["MediaCatId"] = MediaCatId

	if LangName:
		current_language = Language.query\
			.filter(Language.LangName.ilike(f"%{LangName}%"))\
			.first()
		if current_language:
			filtering["LangId"] = current_language.LangId

	db_media = Media.query.filter_by(**filtering)

	if MediaTitle:
		db_media = db_media.filter(Media.MediaTitle.ilike(f"%{MediaTitle}%"))

	if MediaName:
		db_media = db_media.filter(Media.MediaName.ilike(f"%{MediaName}%"))

	if MediaAuthor:
		db_media = db_media.filter(Media.MediaAuthor.ilike(f"%{MediaAuthor}%"))

	if MediaBody:
		db_media = db_media.filter(Media.MediaBody.ilike(f"%{MediaBody}%"))

	if startDate:
		if (type(startDate) != datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate) != datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)

		db_media = db_media\
			.filter(and_(
				extract('year',Media.MediaDate).between(startDate.year,endDate.year),\
				extract('month',Media.MediaDate).between(startDate.month,endDate.month),\
				extract('day',Media.MediaDate).between(startDate.day,endDate.day)))

	db_media = db_media.order_by(Media.MediaDate.desc())

	db_media = db_media.options(
		joinedload(Media.language)
	).all()

	data = []
	for media_data in db_media:
		this_data = media_data.to_json_api()
		this_data["LangName"] = media_data.language.LangName if media_data.language else ""
		data.append(this_data)

	return data