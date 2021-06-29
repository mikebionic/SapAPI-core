
def generate_InterActiv_payload(
	MerchantId,
	TerminalId,
	TotalPrice,
	OInvRegNo,
	OrderDesc = None,
	return_url = None,
	CurrencyNumCode = 840,
	CustomerName = 'Plan Planyev',
	CustomerEmail = None,
	CustomerHomePhone = None,
	CustomerMobilePhone = None,
	UserAgent = None,
	RemoteAddress = None,
	ScreenHeight = 1200,
	ScreenWidth = 1900,
):
	data = {
		"RequestId": "99",
		"Environment": {
			"Merchant": {
				"Id": MerchantId
			},
			"POI": {
				"Id": TerminalId,
				"Language": "en-US"
			},
			"Card": None,
			"CardRecipient": None,
			"Customer": {
				"Name": CustomerName,
				"Language": "en-US",
				"Email": CustomerEmail,
				"HomePhone": None,
				"MobilePhone": None,
			},
			"CustomerDevice": {
				"Browser": {
					"AcceptHeader": "text/html",
					"IpAddress": RemoteAddress,
					"JavaEnabled": False,
					"Language": "en-US",
					"ScreenColorDepth": 24,
					"ScreenHeight": ScreenHeight,
					"ScreenWidth": ScreenWidth,
					"TimeZone": 185,
					"UserAgentString": UserAgent
				},
				"MobileApp": None
			},
			"Transport": {
				"MerchantFinalResponseUrl": return_url,
				"ChallengeResponseUrl": return_url,
				"ChallengeWindowSize": 3,
				"ChallengeResponseData": None,
				"ThreeDSMethodNotificationUrl": "",
				"MethodCompletion": False,
				"Consent": False,
				"EndpointHostAddress": "/orders/7b72093d-bb14-45b5-a6ec-a3ca5f6c2731"
			},
			"SponsoredMerchant": None,
			"SponsoredMerchantPOI": None
		},
		"Transaction": {
			"InvoiceNumber": "Acquirer",
			"Type": "CRDP",
			"AdditionalService": None,
			"TransactionText": None,
			"TotalAmount": TotalPrice,
			"Currency": CurrencyNumCode,
			"CurrencyConversion": None,
			"DetailedAmount": None,
			"AirlineItems": None,
			"MerchantOrderId": OInvRegNo,
			"AutoComplete": True,
			"AntiMoneyLaundering": {
				"SenderName": CustomerName,
				"SenderDateOfBirth": None,
				"SenderPlaceOfBirth": None,
				"NationalIdentifier": None,
				"NationalIdentifierCountry": None,
				"NationalIdentifierExpiry": None,
				"PassportNumber": None,
				"PassportIssuingCountry": None,
				"PassportExpiry": None
			},
			"Instalment": None,
			"MerchantCategoryCode": None
		}
	}

	if CustomerMobilePhone:
		CustomerMobilePhone = configurePhoneNumber(CustomerMobilePhone)
		data["Customer"]["Environment"]["MobilePhone"] = {
			"cc": CustomerMobilePhone[:3],
			"subscriber": CustomerMobilePhone[3:]
		}

	if CustomerHomePhone:
		CustomerHomePhone = configurePhoneNumber(CustomerHomePhone)
		data["Customer"]["Environment"]["HomePhone"] = {
			"cc": CustomerHomePhone[:3],
			"subscriber": CustomerHomePhone[3:]
		}


def configurePhoneNumber(number, with_plus_sign=False):
	number = number.strip().replace(' ','').replace('-','').replace('(','').replace(')','')

	number = f"+{number}" if with_plus_sign and number[0] != "+" else number
	number = number[1:] if not with_plus_sign and number[0] == "+" else number

	return number