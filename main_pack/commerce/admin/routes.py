from flask import render_template, url_for, jsonify, json, session, flash, redirect , request, Response, abort
from flask_login import current_user, login_required
from main_pack import db, babel
from main_pack.commerce.admin import bp

@bp.route("/commerce/admin")
def admin_commerce():
	return "Hello, admin"
