## Register api

> Request register

| **Route**          | **Methods** | **Status** | **Note** |
| ------------------ | :---------: | :--------: | -------- |
| /register-request/ |   **GET**   |   Active   |

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
-------

> Validate the verify_code

| **Route**         | **Methods** | **Status** | **Note** |
| ----------------- | :---------: | :--------: | -------- |
| /verify-register/ |  **POST**   |   Active   |

**Properties**
| **Name** | **Type** | **Description** | **Example**                   |
| -------- | :------: | --------------- | ----------------------------- |
| method   | **str**  |                 | ?method=email or phone_number |

> Payload:

```json
{
	"email": "muhammedjepbarov@gmail.com",
	"verify_code": "285184"
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