# -*- coding: utf-8 -*-
from flask import request

from main_pack.api.v1.resource_api import api
from main_pack.api.v1.resource_api.utils import (
	collect_discount_resource_data,
	collect_ordered_resource_data,
	collect_recommended_resource_data,
)
from main_pack.api.auth.utils import token_required
from main_pack.api.response_handlers import handle_default_response

@api.route("/discount-resources/")
def discount_resources_get():
	limit = request.args.get("limit", None, type=int)
	showInactive = request.args.get("showInactive", None, type=int)
	data = collect_discount_resource_data(limit, showInactive)
	return handle_default_response(data, "Discounts")

@api.route("/recommended-resources/")
@token_required
def recommended_resources_get(user):
	if user["model_type"] != "rp_acc":
		message = "This route is available only for Rp_acc"
		return handle_default_response([], message)

	limit = request.args.get("limit", None, type=int)
	data, message = collect_recommended_resource_data(user['current_user'], limit)
	return handle_default_response(data, message)

@api.route("/ordered-resources/")
def ordered_resources_get():
	ResId = request.args.get("id", None, type=int)
	ResGuid = request.args.get("guid", None, type=str)
	limit = request.args.get("limit", None, type=int)
	data, message = collect_ordered_resource_data(ResId, ResGuid, limit)
	return handle_default_response(data, message)
