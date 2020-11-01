from flask import render_template, url_for, jsonify, session, redirect
from flask import send_from_directory, make_response
from flask_login import current_user, login_required
from sqlalchemy import and_

from main_pack import db, babel, gettext
from main_pack.main import bp
from main_pack import Config

from main_pack.api.commerce.commerce_utils import apiResourceInfo
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


@bp.route("/")
def main():
	# resources_info = apiResourceInfo()
	# resources = resources_info['data']
	categories = Res_category.query\
		.filter_by(GCRecord = None)\
		.join(Resource, Resource.ResCatId == Res_category.ResCatId)\
		.filter(Resource.GCRecord == None)\
		.join(Res_total, Res_total.ResId == Resource.ResId)\
		.filter(and_(
			Res_total.WhId == 1, 
			Res_total.ResTotBalance > 0))\
		.all()
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