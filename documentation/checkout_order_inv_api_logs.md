# current json (update)
```json
{
	"BaseOs": "",
	"Release": "10",
	"Brand": "samsung",
	"Device": "a7y18lte",
	"Display": "QP1A.190711.020.A750FXXU5CUA3",
	"Id": "QP1A.190711.020",
	"Manufacturer": "samsung",
	"Model": "SM-A750F",
	"IsPhysicalDevice": true,
	"AndroidId": "e4d788879fbe6635",
	"orderInv": {
			"OInvTypeId": 2,
			"InvStatId": 1,
			"RpAccGuid": "0f547807-c691-40f1-af0d-4837f1075ddf",
			"PtId": 1,
			"PmId": 1,
			"PaymStatusId": 1,
			"OInvRegNo": "",
			"OInvDesc": "",
			"OrderInvLines": [
					{
							"UnitId": 1,
							"ResId": 36,
							"OInvLineAmount": 3.0,
							"OInvLinePrice": 35.0
					}
			]
	}
}
```


# request json data
```JSON
{
	"BaseOs":"LoremIpsum",
	"Release":"LoremIpsum",
	"Brand":"LoremIpsum",
	"Device":"LoremIpsum",
	"Display":"LoremIpsum",
	"Id":"LoremIpsum",
	"Manufacturer":"LoremIpsum",
	"Model":"LoremIpsum",
	"IsPhysicalDevice":"LoremIpsum",
	"AndroidId":"LoremIpsum",
	"orderInv":{
		"RpAccId":13,
		"InvStatId":"3",
		"OInvDesc":"sdfasdfasdfasdf",
		"OInvDiscountAmount":10,
		"OInvExpenseAmount":22,
		"OInvFTotal":155,
		"OInvRegNo":"LoremIpsum",
		"OInvTypeId":2,
		"OrderInvLines":[
			{
				"ResId":7,
				"OInvLineDesc":"Loasfef333333psum",
				"OInvLineAmount":8,
				"OInvLinePrice":2
			},
			{
				"ResId":4,
				"OInvLineDesc":"LoremIsdjfapsum",
				"OInvLineAmount":3,
				"OInvLinePrice":9999
			},
			{
				"ResId":55,
				"OInvLineDesc":"LoremIpsum",
				"OInvLineAmount":3,
				"OInvLinePrice":10
			}
		]
	}
}
```

# server Response
```JSON
{
	"data": {
		"AddInf1": null,
		"AddInf2": null,
		"AddInf3": null,
		"AddInf4": null,
		"AddInf5": null,
		"AddInf6": null,
		"CId": null,
		"CreatedDate": null,
		"CreatedUId": null,
		"CurrencyId": 1,
		"DivId": null,
		"EmpId": null,
		"GCRecord": null,
		"InvStatId": 1,
		"ModifiedDate": null,
		"ModifiedUId": null,
		"OInvCreditDays": null,
		"OInvCreditDesc": null,
		"OInvDate": null,
		"OInvDesc": "sdfasdfasdfasdf",
		"OInvDiscountAmount": 10,
		"OInvExpenseAmount": 22,
		"OInvFTotal": 155,
		"OInvFTotalInWrite": null,
		"OInvModifyCount": null,
		"OInvPrintCount": null,
		"OInvRegNo": "ARSSFK9989",
		"OInvTaxAmount": null,
		"OInvTotal": null,
		"OInvTypeId": 2,
		"RpAccId": 4,
		"WhId": null,
		"WpId": null
	},
	"fail_total": 2,
	"fails": [
		{
			"data":{
					"OInvLineAmount": 8,
					"OInvLineDesc": "Loasfef333333psum",
					"OInvLinePrice": 2,
					"ResId": 7
				},
			"error_type_id": 2,
			"error_type_message": "Usage satus: Inactive"
		},
		{
			"data":{
				"OInvLineAmount": 3,
				"OInvLineDesc": "LoremIsdjfapsum",
				"OInvLinePrice": 9999,
				"ResId": 4
			},
			"error_type_id": 1,
			"error_type_message": "Deleted"
		}
	],
	"message": "Success and fail",
	"status": 2,
	"successes": [
		{
			"AddInf1": null,
			"AddInf2": null,
			"AddInf3": null,
			"AddInf4": null,
			"AddInf5": null,
			"AddInf6": null,
			"CreatedDate": null,
			"CreatedUId": null,
			"CurrencyId": 1,
			"GCRecord": null,
			"LastVendorId": null,
			"ModifiedDate": null,
			"ModifiedUId": null,
			"OInvId": 73,
			"OInvLineAmount": 3,
			"OInvLineDate": null,
			"OInvLineDesc": "LoremIpsum",
			"OInvLineDiscAmount": 0,
			"OInvLineExpenseAmount": 0,
			"OInvLineFTotal": 30,
			"OInvLineId": null,
			"OInvLinePrice": 10,
			"OInvLineTaxAmount": 0,
			"OInvLineTotal": 30,
			"ResId": 55,
			"UnitId": null
		}
	],
	"success_total": 1,
	"total": 3
}
```


# request specific order inv
```URL
127.0.0.1:5000/api/v-order-invoices/ARSSFK6648/
```
# server response for specific order inv
```JSON
{
    "data": {
        "AddInf1": null,
        "AddInf2": null,
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "CId": null,
        "CreatedDate": "2020-07-14 17:27:20",
        "CreatedUId": null,
        "CurrencyId": 1,
        "DivId": null,
        "EmpId": null,
        "GCRecord": null,
        "InvStatId": 1,
        "ModifiedDate": "2020-07-14 17:27:20",
        "ModifiedUId": null,
        "OInvCreditDays": 0,
        "OInvCreditDesc": null,
        "OInvDate": "2020-07-14 17:27:20",
        "OInvDesc": "sdfasdfasdfasdf",
        "OInvDiscountAmount": 10,
        "OInvExpenseAmount": 22,
        "OInvFTotal": 110,
        "OInvFTotalInWrite": "ýüz on manat nol teňňe",
        "OInvId": 56,
        "OInvModifyCount": 0,
        "OInvPrintCount": 0,
        "OInvRegNo": "ARSSFK6648",
        "OInvTaxAmount": 0,
        "OInvTotal": 110,
        "OInvTypeId": 2,
        "Order_inv_lines": [
            {
                "AddInf1": null,
                "AddInf2": null,
                "AddInf3": null,
                "AddInf4": null,
                "AddInf5": null,
                "AddInf6": null,
                "CreatedDate": "2020-07-14 17:27:20",
                "CreatedUId": null,
                "CurrencyId": 1,
                "GCRecord": null,
                "LastVendorId": null,
                "ModifiedDate": "2020-07-14 17:27:20",
                "ModifiedUId": null,
                "OInvId": 56,
                "OInvLineAmount": 3,
                "OInvLineDate": "2020-07-14 17:27:20",
                "OInvLineDesc": "LoremIpsum",
                "OInvLineDiscAmount": 0,
                "OInvLineExpenseAmount": 0,
                "OInvLineFTotal": 30,
                "OInvLineId": 56,
                "OInvLinePrice": 10,
                "OInvLineTaxAmount": 0,
                "OInvLineTotal": 30,
                "ResId": 55,
                "UnitId": null
            },
            {
                "AddInf1": null,
                "AddInf2": null,
                "AddInf3": null,
                "AddInf4": null,
                "AddInf5": null,
                "AddInf6": null,
                "CreatedDate": "2020-07-14 17:27:20",
                "CreatedUId": null,
                "CurrencyId": 1,
                "GCRecord": null,
                "LastVendorId": null,
                "ModifiedDate": "2020-07-14 17:27:20",
                "ModifiedUId": null,
                "OInvId": 56,
                "OInvLineAmount": 8,
                "OInvLineDate": "2020-07-14 17:27:20",
                "OInvLineDesc": "Loasfef333333psum",
                "OInvLineDiscAmount": 0,
                "OInvLineExpenseAmount": 0,
                "OInvLineFTotal": 80,
                "OInvLineId": 55,
                "OInvLinePrice": 10,
                "OInvLineTaxAmount": 0,
                "OInvLineTotal": 80,
                "ResId": 123,
                "UnitId": null
            }
        ],
        "RpAccId": 4,
        "WhId": null,
        "WpId": null
    },
    "message": "Order lines",
    "status": 1,
    "total": 2
}
```