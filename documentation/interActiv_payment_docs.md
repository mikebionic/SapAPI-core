# InterActiv Payment usage

## 1. Authentication

| url                                 | type  |
| ----------------------------------- | :---: |
| https://ecomt.tfeb.gov.tm/v1/orders | post  |


**Header**
| key          | value                            |
| ------------ | -------------------------------- |
| ClientId     | 1.300000000000012.30000012       |
| CleintSecret | lMoJw5uFN+fPyFaS8XjsuaRNEYzMGRQ= |

**Response header**

```json
{
	"authorization": "Bearer eyJhbGci...",
	"x-powered-by": "ASP.NET",
	"x-ua-compatible": "IE=Edge,chrome=1",
	"date":	"Wed, 09 Jun 2021 12:55:32 GMT",
	"content-length":	0
}
```

---

## 2. Initiate Order


| url                                 | type  |
| ----------------------------------- | :---: |
| https://ecomt.tfeb.gov.tm/v1/orders | post  |


**Header**
| key           | value                |
| ------------- | -------------------- |
| Authorization | Bearer ...           |
| Content-type  | application/json     |
| Accept        | application/hal+json |



**Order minimal payload**

```json

{
  "RequestId": "99",
  "Environment": {
    "Merchant": {
      "Id": "300000000000012"
    },
    "POI": {
      "Id": "30000012",
      "Language": "en-US"
    },
    "Card": null,
    "CardRecipient": null,
    "Customer": {
      "Name": "Plan Planyyew",
      "Language": "en-US",
      "Email": "rmrmr.pspaps@mail.ru",
      "HomePhone": {
        "cc": "916",
        "subscriber": "22555666"
      },
      "MobilePhone": {
        "cc": "916",
        "subscriber": "99777888"
      }
    },
    "CustomerDevice": {
      "Browser": {
        "AcceptHeader": "text/html",
        "IpAddress": "127.0.0.1",
        "JavaEnabled": false,
        "Language": "en-US",
        "ScreenColorDepth": 24,
        "ScreenHeight": 1200,
        "ScreenWidth": 1900,
        "TimeZone": 120,
        "UserAgentString": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.3"
      },
      "MobileApp": null
    },
    "Transport": {
      "MerchantFinalResponseUrl": "http://127.0.0.1:5000/cart/confirm_order",
      "ChallengeResponseUrl": "http://127.0.0.1:5000/cart",
      "ChallengeWindowSize": 3,
      "ChallengeResponseData": null,
      "ThreeDSMethodNotificationUrl": "",
      "MethodCompletion": false,
      "Consent": false,
      "EndpointHostAddress": "/orders/7b72093d-bb14-45b5-a6ec-a3ca5f6c2731"
    },
    "SponsoredMerchant": null,
    "SponsoredMerchantPOI": null
  },
  "Transaction": {
    "InvoiceNumber": "Acquirer",
    "Type": "CRDP",
    "AdditionalService": null,
    "TransactionText": null,
    "TotalAmount": 1.5,
    "Currency": "934",
    "CurrencyConversion": null,
    "DetailedAmount": null,
    "AirlineItems": null,
    "MerchantOrderId": "29",
    "AutoComplete": true,
    "AntiMoneyLaundering": {
      "SenderName": "Plan Planyyew",
      "SenderDateOfBirth": null,
      "SenderPlaceOfBirth": null,
      "NationalIdentifier": null,
      "NationalIdentifierCountry": null,
      "NationalIdentifierExpiry": null,
      "PassportNumber": "123-456",
      "PassportIssuingCountry": null,
      "PassportExpiry": "2022/2/01"
    },
    "Instalment": null,
    "MerchantCategoryCode": null
  }
}
```

MerchantFinalResponseUrl - will redirect browser to it if press "cancel" 
CustomerDevice {} is required to let it redirect



**Response**

```json
{
  "requestId": "99",
  "environment": {
    "merchant": {
      "id": "300000000000012"
    },
    "poi": {
      "id": "30000012",
      "language": "en-US"
    },
    "customer": {
      "name": "Plan Planyyew",
      "language": "en-US",
      "email": "rmrmr.pspaps@mail.ru",
      "homePhone": {
        "cc": "916",
        "subscriber": "22555666"
      },
      "mobilePhone": {
        "cc": "916",
        "subscriber": "99777888"
      }
    },
    "customerDevice": {
      "browser": {
        "acceptHeader": "text/html",
        "ipAddress": "127.0.0.1",
        "javaEnabled": false,
        "language": "en-US",
        "screenColorDepth": 24,
        "screenHeight": 1200,
        "screenWidth": 1900,
        "timeZone": 120,
        "userAgentString": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.3"
      }
    },
    "transport": {
      "merchantFinalResponseUrl": "http://127.0.0.1:5000/cart/confirm_order?",
      "challengeResponseUrl": "http://127.0.0.1:5000/cart",
      "challengeWindowSize": 3,
      "threeDSMethodNotificationUrl": "",
      "methodCompletion": false,
      "consent": false,
      "endpointHostAddress": "https://ecomt.tfeb.gov.tm/v1/Orders"
    }
  },
  "transaction": {
    "invoiceNumber": "Acquirer",
    "type": "CRDP",
    "totalAmount": 1.5,
    "currency": "934",
    "merchantOrderId": "29",
    "autoComplete": true,
    "antiMoneyLaundering": {
      "senderName": "Plan Planyyew",
      "passportNumber": "123-456",
      "passportExpiry": "2022/2/01"
    }
  },
  "response": {
    "orderId": "d794539b-824c-4373-9acc-f3c479e6be15",
    "operationResult": "OPG-00100",
    "operationResultDescription": "Further action is needed."
  },
  "_links": {
    "self": {
      "href": "https://ecomt.tfeb.gov.tm/v1/Orders/d794539b-824c-4373-9acc-f3c479e6be15"
    },
    "redirectToCheckout": {
      "href": "https://ecomt.tfeb.gov.tm/Checkout/d794539b-824c-4373-9acc-f3c479e6be15"
    }
  }
}
```

browser should show window with link taken from response["_links"]["redirectToCheckout"]["href"]
```url
https://ecomt.tfeb.gov.tm/Checkout/d794539b-824c-4373-9acc-f3c479e6be15
```

After acquirer completes or canceles checkout, we will be redirected to page we provided in **MerchantFinalResponseUrl** and **ChallengeResponseUrl**

## Checking order

App should do another request to get the state of order from response["_links"]["self"]["href"]

**Request**

| url                                                                      | type  |
| ------------------------------------------------------------------------ | :---: |
| https://ecomt.tfeb.gov.tm/v1/Orders/d794539b-824c-4373-9acc-f3c479e6be15 |  GET  |

**Header**
| key           | value                |
| ------------- | -------------------- |
| Authorization | Bearer ...           |


**Response**
```json
{
  "environment": {
    "transport": {
      "challengeWindowSize": 0,
      "methodCompletion": false,
      "consent": false,
      "endpointHostAddress": "https://ecomt.tfeb.gov.tm/v1/Orders"
    }
  },
  "transaction": {
    "invoiceNumber": "Acquirer",
    "totalAmount": 1.50,
    "currency": "934",
    "airlineItems": [],
    "merchantOrderId": "29",
    "autoComplete": false
  },
  "response": {
    "orderId": "d794539b-824c-4373-9acc-f3c479e6be15",
    "threeDSecureTransId": "d794539b-824c-4373-9acc-f3c479e6be15",
    "operationResult": "OPG-00006",
    "operationResultDescription": "The merchant cancelled the order."
  }
}
```
**operationResult** should be GEN-00000 - "Operation Successful"

---


**Order payload with keys**

```json
{
	"RequestId": "26ae2420-ad3d-48b5-9964-f29b66a3f34b",
	"Environment": {
		"Merchant": {
			"Id": "<MerchantId>"
		},
		"POI": {
			"Id": "<TerminalId>",
			"Language": "en-US"
		},
		"Card": {
			"PAN": "<Card ID>",
			"ExpiryDate": "<Exp Date>",
			"SecurityCode2": "<CVC>",
			"Name": "<Full Name>",
			"TAVV": null,
			"IsCardOnFile": false
		},
		"CardRecipient": null,
		"Customer": {
			"Name": "<RpAccFullName or RpAccName>",
			"Language": "en-US",
			"Email": "<RpAccEMail>",
			"HomePhone": {
				"cc": "<Country code>",
				"subscriber": "<Number>"
			},
			"MobilePhone": {
				"cc": "<Country code>",
				"subscriber": "<Number>"
			},
			"WorkPhone": {
				"cc": "<Country code>",
				"subscriber": "<Number>"
			}
		},
		"CustomerDevice": {
			"Browser": {
				"AcceptHeader": "*/*",
				"IpAddress": "<IP of browser/device [IPv4 or IPv6]>",
				"JavaEnabled": false,
				"Language": "en-US",
				"ScreenColorDepth": 48,
				"ScreenHeight": "<window.height>",
				"ScreenWidth": "<window.width>",
				"TimeZone": 120,
				"UserAgentString": "Mozilla/5.0 ..."
			},
			"MobileApp": null
		},
		"BillingAddress": {
			"SameAsShipping": true,
			"Line1": "Annex 4",
			"Line2": "1st floor",
			"PostCode": "2020",
			"City": "01",
			"CountrySubdivision": "01",
			"Country": "196"
		},
		"ShippingAddress": {
			"SameAsShipping": false,
			"Line1": "Annex 4",
			"Line2": "1st floor",
			"PostCode": "2020",
			"City": "01",
			"CountrySubdivision": "01",
			"Country": "196"
		},
		"Transport": {
			"MerchantFinalResponseUrl": "http://<url_to>/Order/FinalResponse/<orderId>",
			"ChallengeResponseUrl": "http://<url_to>/Order/NotificationUrl/<orderId>",
			"ChallengeWindowSize": "<screen dimention Id (3)>",
			"ChallengeResponseData": null,
			"ThreeDSMethodNotificationUrl": "http://<url_to>/Order/ThreeDSecureNotificationUrl/<orderId>",
			"MethodCompletion": false,
			"Consent": false,
			"EndpointHostAddress": "/orders/<orderId>"
		},
		"SponsoredMerchant": null,
		"SponsoredMerchantPOI": null
	},
	"Transaction": {
		"InvoiceNumber": "<order/invoice id or RegNo?>",
		"Type": "CRDP",
		"AdditionalService": null,
		"TransactionText": "<OrderDesc>",
		"TotalAmount": "<total price>",
		"Currency": "978",
		"CurrencyConversion": null,
		"DetailedAmount": null,
		"AirlineItems": null,
		"MerchantOrderId": "<orderId>",
		"AutoComplete": false,
		"AntiMoneyLaundering": {
			"SenderName": null,
			"SenderDateOfBirth": null,
			"SenderPlaceOfBirth": null,
			"NationalIdentifier": null,
			"NationalIdentifierCountry": null,
			"NationalIdentifierExpiry": null,
			"PassportNumber": null,
			"PassportIssuingCountry": null,
			"PassportExpiry": null
		},
		"Instalment": null,
		"MerchantCategoryCode": null
	},
	"Response": null
}

```


---

**full example json payload**
```json
{
	"RequestId": "26ae2420-ad3d-48b5-9964-f29b66a3f34b",
	"Environment": {
		"Merchant": {
			"Id": "300000000000049"
		},
		"POI": {
			"Id": "30000004",
			"Language": "en-US"
		},
		"Card": {
			"PAN": "407457. . . . . . .",
			"ExpiryDate": "2409",
			"SecurityCode2": "442",
			"Name": "John Doe",
			"TAVV": null,
			"IsCardOnFile": false
		},
		"CardRecipient": null,
		"Customer": {
			"Name": "John Doe",
			"Language": "en-US",
			"Email": "john.doe@email.com",
			"HomePhone": {
				"cc": "357",
				"subscriber": "22555666"
			},
			"MobilePhone": {
				"cc": "357",
				"subscriber": "99777888"
			},
			"WorkPhone": null
		},
		"CustomerDevice": {
			"Browser": {
				"AcceptHeader": "*/*",
				"IpAddress": "10.33.27.3",
				"JavaEnabled": false,
				"Language": "en-US",
				"ScreenColorDepth": 48,
				"ScreenHeight": 1200,
				"ScreenWidth": 1900,
				"TimeZone": 120,
				"UserAgentString": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.3"
			},
			"MobileApp": null
		},
		"BillingAddress": {
			"SameAsShipping": true,
			"Line1": "Annex 4",
			"Line2": "1st floor",
			"PostCode": "2020",
			"City": "01",
			"CountrySubdivision": "01",
			"Country": "196"
		},
		"ShippingAddress": {
			"SameAsShipping": false,
			"Line1": "Annex 4",
			"Line2": "1st floor",
			"PostCode": "2020",
			"City": "01",
			"CountrySubdivision": "01",
			"Country": "196"
		},
		"Transport": {
			"MerchantFinalResponseUrl": "http://localhost:8160/Order/FinalResponse/87bddd1a -317e-46dc-b0b8-cc9b83257e5a",
			"ChallengeResponseUrl": "http://localhost:8160/Order/NotificationUrl/87bddd1a-317e-46dc-b0b8-cc9b83257e5a",
			"ChallengeWindowSize": 3,
			"ChallengeResponseData": null,
			"ThreeDSMethodNotificationUrl": "http://localhost:8160/Order/ThreeDSecureNotificationUrl/87bddd1a-317e-46dc-b0b8-cc9b83257e5a",
			"MethodCompletion": false,
			"Consent": false,
			"EndpointHostAddress": "/orders/87bddd1a-317e-46dc-b0b8-cc9b83257e5a"
		},
		"SponsoredMerchant": null,
		"SponsoredMerchantPOI": null
	},
	"Transaction": {
		"InvoiceNumber": "1",
		"Type": "CRDP",
		"AdditionalService": null,
		"TransactionText": null,
		"TotalAmount": 15.99,
		"Currency": "978",
		"CurrencyConversion": null,
		"DetailedAmount": null,
		"AirlineItems": null,
		"MerchantOrderId": "87bddd1a-317e-46dc-b0b8-cc9b83257e5a",
		"AutoComplete": false,
		"AntiMoneyLaundering": {
			"SenderName": null,
			"SenderDateOfBirth": null,
			"SenderPlaceOfBirth": null,
			"NationalIdentifier": null,
			"NationalIdentifierCountry": null,
			"NationalIdentifierExpiry": null,
			"PassportNumber": null,
			"PassportIssuingCountry": null,
			"PassportExpiry": null
		},
		"Instalment": null,
		"MerchantCategoryCode": null
	},
	"Response": null
}

```
