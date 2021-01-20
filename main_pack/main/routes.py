from flask import render_template, url_for, jsonify, session, redirect
from flask import send_from_directory, make_response
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from main_pack import db, babel, gettext
from main_pack.main import bp
from main_pack import Config

from main_pack.api.commerce.commerce_utils import apiResourceInfo

from main_pack.models.base.models import Division
from main_pack.models.commerce.models import (
	Res_category,
	Res_total,
	Resource)


@bp.route('/language/<language>')
def set_language(language=None):
	session['language'] = language
	return redirect(url_for('commerce.commerce'))


@bp.route('/theme/<theme>')
def set_theme(theme=None):
	session['theme'] = theme
	return jsonify({'respone':'theme changed'}),200


@bp.route("/" if Config.SHOW_LANDING_PAGE_ON_ROOT and not Config.COMMERCE_URL_PREFIX else "/commercial")
def main():
	division = Division.query.filter_by(DivGuid = Config.C_MAIN_DIVGUID, GCRecord = None).first()
	DivId = division.DivId if division else 1
	avoidQtyCheckup = 1

	Res_Total_subquery = db.session.query(
		Res_total.ResId,
		db.func.sum(Res_total.ResTotBalance).label("ResTotBalance_sum"),
		db.func.sum(Res_total.ResPendingTotalAmount).label("ResPendingTotalAmount_sum"))\
	.filter(Res_total.DivId == DivId)\
	.group_by(Res_total.ResId)\
	.subquery()

	categories = Res_category.query\
		.filter_by(GCRecord = None)\
		.join(Resource, Resource.ResCatId == Res_category.ResCatId)\
		.filter(Resource.GCRecord == None)\
		.outerjoin(Res_Total_subquery, Res_Total_subquery.c.ResId == Resource.ResId)

	if avoidQtyCheckup == 0:
		if Config.SHOW_NEGATIVE_WH_QTY_RESOURCE == False:	
			categories = categories\
				.filter(Res_Total_subquery.c.ResTotBalance_sum > 0)

	categories = categories.order_by(Res_category.ResCatVisibleIndex.asc()).all()

	return render_template ("commerce/landing_pages/ls.com/index.html",title="Lomaý söwda",
		categories=categories)


@bp.route("/fetch_products")
def fetch_products():
	resources_info = apiResourceInfo()
	resources = resources_info['data']
	res = {
		"data": render_template ("commerce/landing_pages/ls.com/fetch_products.html",resources=resources),
		"status": "success" 
	}
	return make_response(jsonify(res), 200)


########################################
def prepare_data(dropdown,page,title):
	template_data={
		'dropdown': dropdown,
		'page': page,
		'title': title,
	}
	return template_data


@bp.route('/robots.txt')
def robots():
	return send_from_directory(
		directory = Config.WEB_CONFIG_DIRECTORY,
		filename="robots.txt",
		as_attachment=False)


@bp.route('/sitemap.xml')
def sitemap():
	return send_from_directory(
		directory = Config.WEB_CONFIG_DIRECTORY,
		filename="sitemap.xml",
		as_attachment=False)