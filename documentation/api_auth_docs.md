## Register api

> Request register

| **Route**          | **Methods** | **Status** | **Note** |
| ------------------ | :---------: | :--------: | -------- |
| /register-request/ |   **GET**   |   Active   |
| /login-request/    |   **GET**   |   Active   |

**Properties**
| **Name** | **Type** | **Description** | **Example**                   |
| -------- | :------: | --------------- | ----------------------------- |
| method   | **str**  |                 | ?method=email or phone_number |

**Header**:
| **Title**   | **Type** | **Description**                       | **Example**         |
| ----------- | :------: | ------------------------------------- | ------------------- |
| Email       | **str**  | add if requests an email method       | example@example.com |
| PhoneNumber | **str**  | add if requests a phone_number method | +99361234567        |

> Response:

```json
{
  "data": {
    "CreatedDate": "2021-11-17 19:38:29",
    "CreatedUId": null,
    "GCRecord": null,
    "ModifiedDate": "2021-11-18 17:28:25",
    "ModifiedUId": null,
    "RegReqExpDate": "Thu, 18 Nov 2021 17:38:30 GMT",
    "RegReqGuid": "c36819ef-8486-4bae-a155-e3ade866042e",
    "RegReqId": 42,
    "RegReqInfo": null,
    "RegReqIpAddress": null,
    "RegReqPhoneNumber": "muhammedjepbarov@gmail.com",
    "RegReqVerified": 0,
    "RegReqVerifyCode": "",
    "SyncDateTime": "2021-11-17 19:38:29"
  },
  "message": "muhammedjepbarov@gmail.com, Profiliňizi hasaba almak üçin görkezmeler e-poçta iberildi\n Talabyňyzyň işjeň ýagdaý wagty 10 (minutes)",
  "status": 1,
  "total": 1
}
```


------

__login request example__

```bash
curl --request GET \
  --url 'http://localhost:5001/ls/api/login-request/?method=email' \
  --header 'Email: muhammedjepbarov@gmail.com' \
```

**response** 
```json
{
	"data": {
		"CreatedDate": "2022-05-30 17:52:07",
		"CreatedUId": null,
		"GCRecord": null,
		"ModifiedDate": "2022-05-30 18:03:34",
		"ModifiedUId": null,
		"RegReqExpDate": "Mon, 30 May 2022 18:13:47 GMT",
		"RegReqGuid": "73224916-2ab8-4186-ad93-383b0aedef5e",
		"RegReqId": 24,
		"RegReqInfo": null,
		"RegReqIpAddress": null,
		"RegReqPhoneNumber": "muhammedjepbarov@gmail.com",
		"RegReqVerified": 0,
		"RegReqVerifyCode": "",
		"SyncDateTime": "2022-05-30 17:52:07"
	},
	"message": "muhammedjepbarov@gmail.com, An email has been sent with instructions to login into your profile\n Talabyňyzyň işjeň ýagdaý wagty 10 (minutes)",
	"status": 1,
	"total": 14
}
```

-------

> Validate the verify_code

| **Route**         | **Methods** | **Status** | **Note** |
| ----------------- | :---------: | :--------: | -------- |
| /verify-register/ |  **POST**   |   Active   |
| /verify-login/    |  **POST**   |   Active   | this will log a user in and return user credentials

**Properties**
| **Name** | **Type** | **Description** | **Example**                   |
| -------- | :------: | --------------- | ----------------------------- |
| method   | **str**  |                 | ?method=email or phone_number |

> Payload:

```json
{
	"email": "muhammedjepbarov@gmail.com",
	"verify_code": "285184",
	// "phone_number": "+99361234567",
}
```

> Response:

```json
{
  "data": {
    "CreatedDate": "2021-11-17 19:38:29",
    "CreatedUId": null,
    "GCRecord": null,
    "ModifiedDate": "2021-11-19 17:55:32",
    "ModifiedUId": null,
    "RegReqExpDate": "Fri, 19 Nov 2021 18:20:58 GMT",
    "RegReqGuid": "c36819ef-8486-4bae-a155-e3ade866042e",
    "RegReqId": 42,
    "RegReqInfo": null,
    "RegReqIpAddress": null,
    "RegReqPhoneNumber": "muhammedjepbarov@gmail.com",
    "RegReqVerified": 1,
    "RegReqVerifyCode": "200253",
    "SyncDateTime": "2021-11-17 19:38:29",
    "email": "muhammedjepbarov@gmail.com",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzczODc4MTgsImlhdCI6MTYzNzMyNzgxOCwibmJmIjoxNjM3MzI3ODE4LCJlbWFpbCI6Im11aGFtbWVkamVwYmFyb3ZAZ21haWwuY29tIn0.xWM0HPZrobTufI5odgXM9bqmvop48lsL6D1SAe32s5Q"
  },
  "message": "muhammedjepbarov@gmail.com, successfully verified",
  "status": 1,
  "total": 1
}
```

> Response Header:

```json
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzczODc4MTgsImlhdCI6MTYzNzMyNzgxOCwibmJmIjoxNjM3MzI3ODE4LCJlbWFpbCI6Im11aGFtbWVkamVwYmFyb3ZAZ21haWwuY29tIn0.xWM0HPZrobTufI5odgXM9bqmvop48lsL6D1SAe32s5Q"}
```

> Use the token from response or header to put on your register API request.
------

> Register user.


| **Route**  | **Methods** | **Status** | **Note**                  |
| ---------- | :---------: | :--------: | ------------------------- |
| /register/ |  **POST**   |   Active   | ?type=rp_acc&method=email |

**Properties**
| **Name** | **Type** | **Description**                | **Example**                   |
| -------- | :------: | ------------------------------ | ----------------------------- |
| type     | **str**  |                                | ?type=rp_acc or user          |
| method   | **str**  |                                | &method=email or phone_number |
| token    | **str**  | token could be added in header | &token=                       |

**Header**:
| **Title** | **Type** | **Description**                 | **Example** |
| --------- | :------: | ------------------------------- | ----------- |
| token     | **str**  | this could be added in url prop |             |

> Payload:

```json
{
	"RpAccUName": "username",
	"RpAccUPass": "password",
	"RpAccAddress": "address",
	"RpAccName": "full_name"
}
```

> Response:

```json
{
  "data": {
    "exp": "2021-11-20 11:11:30",
    "rp_acc": {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CId": 1,
      "CreatedDate": "2021-11-19 18:30:55",
      "CreatedUId": null,
      "DbGuid": null,
      "DeviceQty": null,
      "DivId": 1,
      "EmpId": null,
      "FilePathM": "",
      "FilePathR": "",
      "FilePathS": "",
      "GCRecord": null,
      "GenderId": null,
      "Images": [],
      "IsMain": null,
      "ModifiedDate": "2021-11-19 18:30:55",
      "ModifiedUId": null,
      "NatId": null,
      "ReprId": null,
      "ResPriceGroupId": null,
      "RpAccAddress": "address",
      "RpAccBirthDate": null,
      "RpAccEMail": "muhammedjepbarov@gmail.com",
      "RpAccFirstName": null,
      "RpAccGuid": "154aa458-acd7-49b6-b94d-4b3582d1ec34",
      "RpAccHomePhoneNumber": null,
      "RpAccId": 54,
      "RpAccLangSkills": null,
      "RpAccLastActivityDate": "2021-11-19 18:31:29",
      "RpAccLastActivityDevice": "Browser: None, Platform: None, Details: insomnia/2021.3.0",
      "RpAccLastName": null,
      "RpAccLatitude": 0.0,
      "RpAccLongitude": 0.0,
      "RpAccMobilePhoneNumber": null,
      "RpAccName": "full_name",
      "RpAccPassportIssuePlace": null,
      "RpAccPassportNo": null,
      "RpAccPatronomic": null,
      "RpAccPurchBalanceLimit": 0.0,
      "RpAccRegNo": "ARAK16",
      "RpAccResidency": null,
      "RpAccSaleBalanceLimit": 0.0,
      "RpAccStatusId": 1,
      "RpAccTypeId": 2,
      "RpAccUName": "username",
      "RpAccViewCnt": null,
      "RpAccVisibleIndex": null,
      "RpAccWebAddress": null,
      "RpAccWorkFaxNumber": null,
      "RpAccWorkPhoneNumber": null,
      "RpAccZipCode": null,
      "Rp_acc_status": {
        "CreatedDate": null,
        "CreatedUId": 0,
        "GCRecord": null,
        "ModifiedDate": null,
        "ModifiedUId": 0,
        "RpAccStatusDesc": "",
        "RpAccStatusGuid": null,
        "RpAccStatusId": 1,
        "RpAccStatusName": "Işlewde",
        "SyncDateTime": null
      },
      "Rp_acc_type": {
        "CreatedDate": null,
        "CreatedUId": 0,
        "GCRecord": null,
        "ModifiedDate": null,
        "ModifiedUId": 0,
        "RpAccTypeDesc": "",
        "RpAccTypeGuid": null,
        "RpAccTypeId": 2,
        "RpAccTypeName": "Alyjy",
        "SyncDateTime": null
      },
      "SyncDateTime": "2021-11-19 18:30:55",
      "UnusedDeviceQty": null,
      "User": {
        "AddInf1": null,
        "AddInf2": null,
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 18:53:03",
        "CreatedUId": null,
        "DivId": 1,
        "EmpId": null,
        "GCRecord": null,
        "ModifiedDate": "2020-11-07 23:21:46",
        "ModifiedUId": null,
        "ResPriceGroupId": null,
        "RpAccId": 36,
        "SyncDateTime": "2020-10-27 18:53:03",
        "UEmail": "muhammedjepbarov@gmail.com",
        "UFullName": "Mike Bionic",
        "UGuid": null,
        "UId": 3,
        "ULastActivityDate": "2021-01-13 07:08:31",
        "ULastActivityDevice": "",
        "UName": "administrator",
        "URegNo": null,
        "UShortName": "AR",
        "UTypeId": 1
      },
      "WpId": null
    },
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzczODg2OTAsImlhdCI6MTYzNzMyODY5MCwibmJmIjoxNjM3MzI4NjkwLCJScEFjY0lkIjo1NH0.x4EMkoGxSaWmxpY4a5OZ0kjOeyEJQGRM4-txcJ9K7-w"
  },
  "message": "username, profiliňiz döredildi!",
  "status": 1,
  "total": 1
}
```

> Response Header:

```json
{
  "Authorization":	"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzczODg2OTAsImlhdCI6MTYzNzMyODY5MCwibmJmIjoxNjM3MzI4NjkwLCJScEFjY0lkIjo1NH0.x4EMkoGxSaWmxpY4a5OZ0kjOeyEJQGRM4-txcJ9K7-w",
  "Set-Cookie": "session=e9456bd1-48d8-4e18-9ce1-15dd390f8108; Expires=Mon, 20 Dec 2021 13:31:30 GMT; HttpOnly; Path=/"
}
```

> Use the token from response or header to login the applications and make a request


------

__login_verify_example__

```bash
curl --request POST \
  --url 'http://localhost:5001/ls/api/verify-login/?method=email' \
  --header 'Content-Type: application/json' \
  --data '{
	"email": "muhammedjepbarov@gmail.com",
	"verify_code": "234097"
}'
```

**response**

```json
{
	"exp": "2022-05-30 18:23:59",
	"message": "Login success!",
	"rp_acc": {
		"AddInf1": null,
		"AddInf2": null,
		"AddInf3": null,
		"AddInf4": null,
		"AddInf5": null,
		"AddInf6": null,
		"CId": 1,
		"CreatedDate": "2021-04-11 02:06:52",
		"CreatedUId": null,
		"DbGuid": null,
		"DeviceQty": null,
		"DivId": 1,
		"EmpId": null,
		"FilePathM": "/ls/api/get-image/image/M/fb824e1f8702510c2a62ef27b0b0.jpg",
		"FilePathR": "/ls/api/get-image/image/R/fb824e1f8702510c2a62ef27b0b0.jpg",
		"FilePathS": "/ls/api/get-image/image/S/fb824e1f8702510c2a62ef27b0b0.jpg",
		"GCRecord": null,
		"GenderId": null,
		"Images": [
			{
				"BrandId": null,
				"CId": null,
				"CreatedDate": "2021-06-24 20:08:45",
				"CreatedUId": null,
				"EmpId": null,
				"FileHash": null,
				"FileName": "523393197f43e41fb56a62721b79.jpg",
				"FilePath": "/ls/api/get-image/image/M/523393197f43e41fb56a62721b79.jpg",
				"FilePathM": "/ls/api/get-image/image/M/523393197f43e41fb56a62721b79.jpg",
				"FilePathR": "/ls/api/get-image/image/R/523393197f43e41fb56a62721b79.jpg",
				"FilePathS": "/ls/api/get-image/image/S/523393197f43e41fb56a62721b79.jpg",
				"GCRecord": null,
				"ImgGuid": "8b386d42-e324-49f4-a3fa-b34ecb28f1e0",
				"ImgId": 59,
				"MaxDarkFileName": "",
				"MaxDarkFilePath": "",
				"MaxLightFileName": "",
				"MaxLightFilePath": "",
				"MinDarkFileName": "",
				"MinDarkFilePath": "",
				"MinLightFileName": "",
				"MinLightFilePath": "",
				"ModifiedDate": "2021-06-24 20:08:45",
				"ModifiedUId": null,
				"ProdId": null,
				"ResCatId": null,
				"ResId": null,
				"RpAccId": 44,
				"SyncDateTime": "2021-06-24 20:08:45",
				"UId": null
			},
			{
				"BrandId": null,
				"CId": null,
				"CreatedDate": "2021-06-24 20:34:54",
				"CreatedUId": null,
				"EmpId": null,
				"FileHash": null,
				"FileName": "fb824e1f8702510c2a62ef27b0b0.jpg",
				"FilePath": "/ls/api/get-image/image/M/fb824e1f8702510c2a62ef27b0b0.jpg",
				"FilePathM": "/ls/api/get-image/image/M/fb824e1f8702510c2a62ef27b0b0.jpg",
				"FilePathR": "/ls/api/get-image/image/R/fb824e1f8702510c2a62ef27b0b0.jpg",
				"FilePathS": "/ls/api/get-image/image/S/fb824e1f8702510c2a62ef27b0b0.jpg",
				"GCRecord": null,
				"ImgGuid": "e33c2e0f-3c7b-499b-a4c4-2ea2e728ed00",
				"ImgId": 60,
				"MaxDarkFileName": "",
				"MaxDarkFilePath": "",
				"MaxLightFileName": "",
				"MaxLightFilePath": "",
				"MinDarkFileName": "",
				"MinDarkFilePath": "",
				"MinLightFileName": "",
				"MinLightFilePath": "",
				"ModifiedDate": "2021-06-24 20:34:54",
				"ModifiedUId": null,
				"ProdId": null,
				"ResCatId": null,
				"ResId": null,
				"RpAccId": 44,
				"SyncDateTime": "2021-06-24 20:34:54",
				"UId": null
			}
		],
		"IsMain": null,
		"ModifiedDate": "2022-05-29 13:33:30",
		"ModifiedUId": null,
		"NatId": null,
		"ReprId": null,
		"ResPriceGroupId": null,
		"RpAccAddress": "plan yerde",
		"RpAccBirthDate": null,
		"RpAccEMail": "muhammedjepbarov@gmail.com",
		"RpAccFirstName": null,
		"RpAccGuid": "954edbe5-049a-455d-a7ab-0729a18affbf",
		"RpAccHomePhoneNumber": "5512312312",
		"RpAccId": 44,
		"RpAccLangSkills": null,
		"RpAccLastActivityDate": "2022-03-24 16:27:48",
		"RpAccLastActivityDevice": "Browser: chrome, Platform: macos, Details: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
		"RpAccLastName": null,
		"RpAccLatitude": 0.0,
		"RpAccLongitude": 0.0,
		"RpAccMobilePhoneNumber": "123",
		"RpAccName": "qd23d23",
		"RpAccPassportIssuePlace": null,
		"RpAccPassportNo": null,
		"RpAccPatronomic": null,
		"RpAccPurchBalanceLimit": 0.0,
		"RpAccRegNo": "MaASK2",
		"RpAccResidency": null,
		"RpAccSaleBalanceLimit": 0.0,
		"RpAccStatusId": 1,
		"RpAccTypeId": 2,
		"RpAccUName": "mike",
		"RpAccViewCnt": 6363,
		"RpAccVisibleIndex": null,
		"RpAccWebAddress": "www.fuckyou.com.tm",
		"RpAccWorkFaxNumber": "34434",
		"RpAccWorkPhoneNumber": "999999123",
		"RpAccZipCode": "dunno88a",
		"Rp_acc_status": {
			"CreatedDate": null,
			"CreatedUId": 0,
			"GCRecord": null,
			"ModifiedDate": null,
			"ModifiedUId": 0,
			"RpAccStatusDesc": "",
			"RpAccStatusGuid": null,
			"RpAccStatusId": 1,
			"RpAccStatusName": "Işlewde",
			"SyncDateTime": null
		},
		"Rp_acc_type": {
			"CreatedDate": null,
			"CreatedUId": 0,
			"GCRecord": null,
			"ModifiedDate": null,
			"ModifiedUId": 0,
			"RpAccTypeDesc": "",
			"RpAccTypeGuid": null,
			"RpAccTypeId": 2,
			"RpAccTypeName": "Alyjy",
			"SyncDateTime": null
		},
		"SyncDateTime": "2021-04-11 02:06:52",
		"UnusedDeviceQty": null,
		"User": {
			"AddInf1": null,
			"AddInf2": null,
			"AddInf3": null,
			"AddInf4": null,
			"AddInf5": "5c3085c6fe8e8897",
			"AddInf6": "5c3085c6fe8e8897",
			"CId": 1,
			"CreatedDate": "2020-10-27 17:39:11",
			"CreatedUId": null,
			"DivId": 1,
			"EmpId": null,
			"GCRecord": null,
			"ModifiedDate": "2021-02-07 14:05:47",
			"ModifiedUId": null,
			"ResPriceGroupId": 7,
			"RpAccId": null,
			"SyncDateTime": "2020-10-27 17:39:11",
			"UEmail": "mekangara@gmail.com",
			"UFullName": "Garayew mekan garayewich",
			"UGuid": "ef393065-e2d9-43a1-9de2-3ba5652d8a57",
			"UId": 1,
			"ULastActivityDate": "2021-01-13 07:08:31",
			"ULastActivityDevice": "",
			"UName": "Mekan Gara",
			"URegNo": "Fuck you",
			"UShortName": "Ma",
			"UTypeId": 1
		},
		"WpId": null
	},
	"status": 1,
	"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTM5MTcwMzksImlhdCI6MTY1MzkxNTgzOSwibmJmIjoxNjUzOTE1ODM5LCJScEFjY0lkIjo0NH0.uwBpU8GNeuxgYKsWn17PIIL7rLrVh3ReepQReJp81ZQ"
}
```

------

# Reset Password api

Step by step workflow for "Forgot password" option:

  [1] Login request: /login-request/
  [2] Verify register: /verify-login/
  [3] Reset Password: /reset-password/

> reset password.

| **Route**  | **Methods** | **Status** | **Note**                  |
| ---------- | :---------: | :--------: | ------------------------- |
| /reset-password/ |  **POST**   |   Active   | ?type=rp_acc, **token_required** |

**Properties**
| **Name** | **Type** | **Description**                | **Example**                   |
| -------- | :------: | ------------------------------ | ----------------------------- |
| type     | **str**  |                                | ?type=rp_acc or user          |

**Header**:
| **Title** | **Type** | **Description**                 | **Example** |
| --------- | :------: | ------------------------------- | ----------- |
| x-access-token     | **str**  | can be as Authorization Bearer |     |

> Payload:

```json
{
	"password": "password",
	"confirm_password": "password",
}
```

> Response:

```json
{
	"data": {
		"RpAccMobilePhoneNumber": "123",
		"RpAccName": "qd23d23",
		...
    "RpAccUName": "mike",
		"RpAccUPass": "123",
		"WpId": null
	},
	"message": "Passwords successfully updated!",
	"status": 1,
	"total": 56
}
```
--------------------------------

