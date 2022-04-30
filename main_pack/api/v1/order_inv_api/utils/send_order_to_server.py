from main_pack.api.common import send_data_to_sync_server

from main_pack.models import (
	Warehouse,
	Resource,
	Rp_acc,
	User,
	Division,
	Currency,
)
from main_pack import Config
from main_pack.base.priceMethods import price_currency_conversion


def send_order_to_server(
	data,
	dbModel = None,
	host = None,
	port = None,
	url_path = None,
	token = None
):
	try:
		if dbModel:
			current_currency = dbModel.currency.CurrencyCode
			payload = dbModel.to_json_api()
			payload["OInvGuid"] = str(payload["OInvGuid"])
			payload["UGuid"] = str(dbModel.user.UGuid)
			payload["RpAccGuid"] = str(dbModel.rp_acc.RpAccGuid)
			payload["DivGuid"] = str(dbModel.division.DivGuid)
			payload["WhGuid"] = str(dbModel.warehouse.WhGuid)

			if Config.CONVERT_CURRENCY_ON_SYNCH:
				payload["OInvFTotal"], payload["CurrencyCode"] = convert_main_currency_price(dbModel.OInvFTotal, current_currency)
				payload["OInvTotal"], payload["CurrencyCode"] = convert_main_currency_price(dbModel.OInvTotal, current_currency)
				payload["OInvFTotalInWrite"] = ""

			inv_lines_payload = []
			for inv_line in dbModel.Order_inv_line:
				current_inv_line = inv_line.to_json_api()
				current_inv_line["OInvLineGuid"] = str(current_inv_line["OInvLineGuid"])
				current_inv_line["ResGuid"] = str(inv_line.resource.ResGuid)

				if Config.CONVERT_CURRENCY_ON_SYNCH:
					current_inv_line["OInvLinePrice"], current_inv_line["CurrencyCode"] = convert_main_currency_price(inv_line.OInvLinePrice, current_currency)
					current_inv_line["OInvLineFTotal"], current_inv_line["CurrencyCode"] = convert_main_currency_price(inv_line.OInvLineFTotal, current_currency)
					current_inv_line["OInvLineTotal"], current_inv_line["CurrencyCode"] = convert_main_currency_price(inv_line.OInvLineTotal, current_currency)
				inv_lines_payload.append(current_inv_line)
			payload["Order_inv_lines"] = inv_lines_payload

		else:
			if data["status"] != 1:
				raise Exception

			payload = data["data"]

			this_warehouse = Warehouse.query.get(payload["WhId"])
			if this_warehouse:
				payload["WhGuid"] = str(this_warehouse.WhGuid)

			this_rp_acc = Rp_acc.query.get(payload["RpAccId"])
			if this_rp_acc:
				payload["RpAccGuid"] = str(this_rp_acc.RpAccGuid)

			this_user = User.query.get(payload["UId"])
			if this_user:
				payload["UGuid"] = str(this_user.UGuid)

			this_division = Division.query.get(payload["DivId"])
			if this_division:
				payload["DivGuid"] = str(this_division.DivGuid)

			current_currency = Currency.query.get(payload["CurrencyId"])

			if Config.CONVERT_CURRENCY_ON_SYNCH:
				payload["OInvFTotal"], payload["CurrencyCode"] = convert_main_currency_price(payload['OInvFTotal'], current_currency)
				payload["OInvTotal"], payload["CurrencyCode"] = convert_main_currency_price(payload['OInvTotal'], current_currency)
				payload["OInvFTotalInWrite"] = ""

			inv_lines_payload = []
			for inv_line in data["successes"]:
				current_inv_line = inv_line.copy()

				this_resource = Resource.query.get(inv_line["ResId"])
				if this_resource:
					current_inv_line["ResGuid"] = str(this_resource.ResGuid)

					if Config.CONVERT_CURRENCY_ON_SYNCH:
						current_inv_line["OInvLinePrice"], current_inv_line["CurrencyCode"] = convert_main_currency_price(current_inv_line['OInvLinePrice'], current_currency)
						current_inv_line["OInvLineFTotal"], current_inv_line["CurrencyCode"] = convert_main_currency_price(current_inv_line['OInvLineFTotal'], current_currency)
						current_inv_line["OInvLineTotal"], current_inv_line["CurrencyCode"] = convert_main_currency_price(current_inv_line['OInvLineTotal'], current_currency)
					inv_lines_payload.append(current_inv_line)

			payload["Order_inv_lines"] = inv_lines_payload

		print(payload)
		send_data_to_sync_server(payload, host, port, url_path, token)

	except Exception as ex:
		print(ex)


def convert_main_currency_price(priceValue, current_currency, to_currency=Config.MAIN_CURRENCY_CODE):
	if current_currency == to_currency:
		return priceValue, current_currency
	price_data = price_currency_conversion(
		priceValue = priceValue,
		from_currency = current_currency,
		to_currency = to_currency)
	return price_data["ResPriceValue"], price_data["CurrencyCode"]