# -*- coding: utf-8 -*-
from sqlalchemy import and_, extract
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
	language = None,
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

	if language:
		current_language = Language.query.filter_by(LangName = language).first()
		if current_language:
			filtering["LangId"] = current_language.LangId

	medias = Media.query.filter_by(**filtering)

	if MediaTitle:
		medias = medias.filter(Media.MediaTitle.ilike(f"%{MediaTitle}%"))

	if MediaName:
		medias = medias.filter(Media.MediaName.ilike(f"%{MediaName}%"))

	if MediaAuthor:
		medias = medias.filter(Media.MediaAuthor.ilike(f"%{MediaAuthor}%"))

	if MediaBody:
		medias = medias.filter(Media.MediaBody.ilike(f"%{MediaBody}%"))

	if startDate:
		if (type(startDate) != datetime):
			startDate = dateutil.parser.parse(startDate)
			startDate = datetime.date(startDate)
		if (type(endDate) != datetime):
			endDate = dateutil.parser.parse(endDate)
			endDate = datetime.date(endDate)

		medias = medias\
			.filter(and_(
				extract('year',Media.MediaDate).between(startDate.year,endDate.year),\
				extract('month',Media.MediaDate).between(startDate.month,endDate.month),\
				extract('day',Media.MediaDate).between(startDate.day,endDate.day)))

	medias = medias.order_by(Media.MediaDate.desc())

	medias = medias.all()

	data = [media.to_json_api() for media in medias]

	return data