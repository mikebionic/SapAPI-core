
[
	{
		"RpAccId": 101004,
		"CId": 0,
		"DivId": 0,
		"UId": 0,
		"EmpId": 0,
		"GenderId": 0,
		"NatId": 0,
		"RpAccStatusId": 0,
		"ReprId": 0,
		"RpAccTypeId": 2,
		"WpId": 0,
		"RpAccRegNo": "A00000124",
		"RpAccName": "Nagt satuw",
		"RpAccAddress": "",
		"RpAccMobilePhoneNumber": "",
		"RpAccHomePhoneNumber": "",
		"RpAccWorkPhoneNumber": "",
		"RpAccWorkFaxNumber": "",
		"RpAccZipCode": null,
		"RpAccEMail": null,
		"RpAccFirstName": null,
		"RpAccLastName": null,
		"RpAccPatronomic": null,
		"RpAccBirthDate":"0001-01-01T00:00:00",
		"RpAccResidency": null,
		"RpAccPassportNo": null,
		"RpAccPassportIssuePlace": null,
		"RpAccLangSkills": null,
		"RpAccSaleBalanceLimit": 0.0,
		"RpAccPurchBalanceLimit": 0.0,
		"AddInf1": "",
		"AddInf2": "",
		"AddInf3": "",
		"AddInf4": "",
		"AddInf5": "",
		"AddInf6": "",
		"CreatedDate": "0001-01-01T00:00:00",
		"ModifiedDate": "0001-01-01T00:00:00",
		"CreatedUId": 0,
		"ModifiedUId": 0
	}
]

# API authentication
/api/login/users/
/api/login/rp-accs/

GET POST
/api/tbl-dk-barcodes/

GET POST
/api/tbl-dk-categories/

GET PUT
/api/tbl-dk-categories/<int:ResCatId>/

GET
/api/tbl-dk-tbl-dk-categories/paginate/

GET POST
/api/tbl-dk-resources/

GET PUT
/api/tbl-dk-resources/<int:ResId>/

GET
/api/v-resources/
/api/v-full-resources/

GET
/api/tbl-dk-categories/<int:ResCatId>/v-resources/

GET
/api/paginate/v-resources/?last=<lastId>&limit=<quantity>

GET POST
/api/tbl-dk-res-prices/

GET POST
/api/tbl-dk-res-totals/

GET POST
/api/tbl-dk-images/

GET POST
/api/tbl-dk-rp-accs/

GET POST
/api/tbl-dk-rp-acc-trans-totals/
/api/tbl-dk-total-transactions/

GET POST
/api/tbl-dk-order-invoices/

GET POST
/api/tbl-dk-order-inv-lines/

GET POST
/api/tbl-dk-order-inv-types/

GET POST
/api/tbl-dk-users/

GET
/api/tbl-dk-users/<int:UId>/

GET POST
/api/tbl-dk-sliders/