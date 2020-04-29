from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db, babel, gettext
from main_pack.main import bp

@bp.route('language/<language>')
def set_language(language=None):
	session['language'] = language
	return redirect(url_for('commerce.commerce'))

@bp.route('/theme/<theme>')
def set_theme(theme=None):
	session['theme'] = theme
	return jsonify({'respone':'theme changed'}),200


# @bp.route("/main")
# @login_required
# def main():
# 	return render_template ("main/main.html", title=gettext("Main window"))

########################################
def prepare_data(dropdown,page,title):
	template_data={
		'dropdown': dropdown,
		'page': page,
		'title': title,
	}
	return template_data