# -*- coding: utf-8 -*-
from flask import request, make_response, jsonify

from main_pack.api.v1.resource_api import api
from main_pack.api.v1.resource_api.utils import (
	collect_discount_resource_data,
	collect_ordered_resource_data,
	# collect_similar_resource_data/
)
from main_pack.api.response_handlers import handle_default_response

@api.route("/similar-resources/")
def similar_resources_get():
	limit = request.args.get("limit", None, type=int)
	showInactive = request.args.get("showInactive", None, type=int)
	data={}
	# data = collect_similar_resource_data(limit, showInactive)
	return handle_default_response(data, "Similar resources")


@api.route("/discount-resources/")
def discount_resources_get():
	limit = request.args.get("limit", None, type=int)
	showInactive = request.args.get("showInactive", None, type=int)
	data = collect_discount_resource_data(limit, showInactive)
	return handle_default_response(data, "Discounts")

@api.route("/recommended-resources/")
def recommended_resources_get():
	ResId = request.args.get("id", None, type=int)
	ResGuid = request.args.get("guid", None, type=int)
	limit = request.args.get("limit", None, type=int)
	showInactive = request.args.get("showInactive", None, type=int)
	data = collect_discount_resource_data(limit, showInactive)
	return handle_default_response(data, "Recommented resources")


@api.route("/ordered-resources/")
def ordered_resources_get():
	ResId = request.args.get("id", None, type=int)
	ResGuid = request.args.get("guid", None, type=int)
	limit = request.args.get("limit", None, type=int)
	data = collect_ordered_resource_data(ResId, ResGuid, limit)
	return handle_default_response(data, "With this product people also buy")
