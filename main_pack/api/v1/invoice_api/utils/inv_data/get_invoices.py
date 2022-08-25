from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from main_pack.config import Config
import dateutil.parser
from main_pack.base.priceMethods import calculatePriceByGroup, price_currency_conversion, configureDecimal
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload
from main_pack.models import (
	Invoice,
    User,
    Rp_acc,
    Inv_line,
    Currency,
    Exc_rate,
	Resource,
)

def get_invoices(DivId = None,
	startDate = None,
	endDate = datetime.now(),
	statusId = None,
	single_object = False,
	invoice_list = None,
	invoice_models = None,
	invoices_only = False,
	show_inv_line_resource = False,
	rp_acc_user = None,
	notDivId = None,
	currency_code = Config.DEFAULT_VIEW_CURRENCY_CODE,
	limit_by = None,
	UId = None,
	RpAccId = None,
	UGuid = None,
	RpAccGuid = None,
	invoices_to_exclude = None,
):

    currencies = Currency.query.filter_by(GCRecord = None).all()
    exc_rates = Exc_rate.query.filter_by(GCRecord = None).all()
    filtering = {"GCRecord": None}
	
    if statusId:
        filtering["InvStatId"] = statusId
    if rp_acc_user:
        filtering["RpAccId"] = rp_acc_user.RpAccId
    if DivId:
        filtering["DivId"] = DivId
    if RpAccId:
        filtering["RpAccId"] = RpAccId

    if UGuid:
        this_user = User.query.filter_by(UGuid = UGuid).first()
        if this_user:
            filtering["UId"] = this_user.UId
    if RpAccGuid:
        tihs_rp_acc = Rp_acc.query.filter_by(RpAccGuid = RpAccGuid).first()
        if tihs_rp_acc:
            filtering["RpAccId"] = tihs_rp_acc.RpAccId

    if UId:
        filtering["UId"] = UId

  
    guid_not_synched_invoices = None
   
    
    if invoices_to_exclude:
        try:
            guids_to_exclude = [inv["InvGuid"] for inv in invoices_to_exclude]
            # modify_dates_to_check = [inv["ModifiedDate"] for inv in invoices_to_exclude]
            invoices = Invoice.query.filter(Invoice.InvGuid.notin_(guids_to_exclude)).all()
            # invoices.extend(guid_not_synched_invoices)
            # invoices = invoices.order_by(Invoice.InvDate.desc())\
            #     .options(
            #     joinedload(Invoice.rp_acc),
            #     joinedload(Invoice.company),
            #     joinedload(Invoice.warehouse),
            #     joinedload(Invoice.division),
            #     joinedload(Invoice.Inv_line)\
            #         .options(
            #             joinedload(Inv_line.resource)
            #         ))
            for inv_to_exclude in invoices_to_exclude:
                thisinvGuid = inv_to_exclude["InvGuid"]
                thisinvModifiedDate = inv_to_exclude["ModifiedDate"]
                if type(thisinvModifiedDate)==datetime:
                    thisinvModifiedDate = dateutil.parser.parse(thisinvModifiedDate)
                thisinv=Invoice.query\
                        .filter(
                            Invoice.InvGuid == thisinvGuid,
                            Invoice.GCRecord == None,
                            Invoice.ModifiedDate > thisinvModifiedDate\
                        ).first()
                if thisinv:
                    print(thisinv)
                    invoices.append(thisinv)
          
        except:
            print("something went wrong")
            pass
    # invoices = invoices.all()
   
    data=[]
   
    for invoice in invoices:
        inv_info = invoice.to_json_api()
        currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == invoice.CurrencyId]
        if not currency_data:
            currency_data = [{"CurrencyCode": Config.DEFAULT_VIEW_CURRENCY_CODE}]
        this_Total = inv_info["InvTotal"]
        this_FTotal = inv_info["InvFTotal"]
        this_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None
        price_data = price_currency_conversion(
            priceValue = this_Total,
            from_currency = this_currencyCode,
            to_currency = currency_code,
            currencies_dbModel = currencies,
            exc_rates_dbModel = exc_rates)
        FTotal_price_data = price_currency_conversion(
            priceValue = this_FTotal,
            from_currency = this_currencyCode,
            to_currency = currency_code,
            currencies_dbModel = currencies,
            exc_rates_dbModel = exc_rates)
        inv_info["InvTotal"] = price_data["ResPriceValue"]
        inv_info["InvFTotal"] = FTotal_price_data["ResPriceValue"]
        inv_info["CurrencyId"] = price_data["CurrencyId"]
        inv_info["CurrencyCode"] = price_data["CurrencyCode"]
        inv_info["CurrencySymbol"] = price_data["CurrencySymbol"]
        rp_acc_data = {}
        if rp_acc_user:
            rp_acc_data = rp_acc_user.to_json_api()
        elif invoice.rp_acc:
            rp_acc_data = invoice.rp_acc.to_json_api()
        inv_info["Rp_acc"] = rp_acc_data
        inv_info["RpAccName"] = rp_acc_data["RpAccName"] if rp_acc_data else ""
        # inv_info["UGuid"] = invoice.user.UGuid if invoice.user and not invoice.user.GCRecord else None
        # inv_info["UName"] = invoice.user.UName if invoice.user and not invoice.user.GCRecord else None
        inv_info["CGuid"] = invoice.company.CGuid if invoice.company and not invoice.company.GCRecord else None
        inv_info["WhGuid"] = invoice.warehouse.WhGuid if invoice.warehouse and not invoice.warehouse.GCRecord else None
        inv_info["DivGuid"] = invoice.division.DivGuid if invoice.division and not invoice.division.GCRecord else None
        inv_info["RpAccGuid"] = invoice.rp_acc.RpAccGuid if invoice.rp_acc and not invoice.rp_acc.GCRecord else None
        inv_info["RpAccRegNo"] = invoice.rp_acc.RpAccRegNo if invoice.rp_acc and not invoice.rp_acc.GCRecord else None
        
        inv_lines = []

        for inv_line in invoice.Inv_line:
            # this_inv_line = inv_line.to_json_api()
            if not inv_line.GCRecord:
                this_inv_line = inv_line.to_json_api()
                this_inv_line["ResRegNo"] = inv_line.resource.ResRegNo if inv_line.resource and not inv_line.resource.GCRecord else None
                this_inv_line["ResGuid"] = inv_line.resource.ResGuid if inv_line.resource and not inv_line.resource.GCRecord else None
                this_inv_line["ResName"] = inv_line.resource.ResName if inv_line.resource and not inv_line.resource.GCRecord else None
                currency_data = [currency.to_json_api() for currency in currencies if currency.CurrencyId == inv_line.CurrencyId]
                if not currency_data:
                    currency_data = [{"CurrencyCode": Config.DEFAULT_VIEW_CURRENCY_CODE}]
                    # print("order_inv_api line exception: no currency specified")
                    # raise Exception
                this_line_Price = this_inv_line["InvLinePrice"]
                this_line_Total = this_inv_line["InvLineTotal"]
                this_line_FTotal = this_inv_line["InvLineFTotal"]
                this_line_currencyCode = currency_data[0]["CurrencyCode"] if currency_data else None
                ExcRateValue = this_inv_line["ExcRateValue"]
                price_data = price_currency_conversion(
                    priceValue = this_line_Price,
                    from_currency = this_line_currencyCode,
                    to_currency = currency_code,
                    currencies_dbModel = currencies,
                    exc_rates_dbModel = exc_rates)
                Total_price_data = price_currency_conversion(
                    priceValue = this_line_Total,
                    from_currency = this_line_currencyCode,
                    to_currency = currency_code,
                    currencies_dbModel = currencies,
                    exc_rates_dbModel = exc_rates)
                FTotal_price_data = price_currency_conversion(
                    priceValue = this_line_FTotal,
                    from_currency = this_line_currencyCode,
                    to_currency = currency_code,
                    currencies_dbModel = currencies,
                    exc_rates_dbModel = exc_rates)
                this_inv_line["InvLinePrice"] = price_data["ResPriceValue"]
                this_inv_line["CurrencyId"] = price_data["CurrencyId"]
                this_inv_line["CurrencyCode"] = price_data["CurrencyCode"]
                this_inv_line["CurrencySymbol"] = price_data["CurrencySymbol"]
                this_inv_line["InvLineTotal"] = Total_price_data["ResPriceValue"]
                this_inv_line["InvLineFTotal"] = FTotal_price_data["ResPriceValue"]
               
                inv_lines.append(this_inv_line)
            # inv_lines.append("sadas")
        inv_info["inv_lines"] = inv_lines
    



        data.append(inv_info)
    res = {
			"message": "Invoice",
			"data": data,
			"total": len(data)
	}
    return res