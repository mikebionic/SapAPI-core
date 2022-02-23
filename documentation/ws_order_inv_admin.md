
> Login request api 

```bash
curl --request GET \
  --url 'http://<host+port>/<prefix>/login/?type=user' \
  --header 'Authorization: Basic YWRtaW46MTIz'
```

> Response

```json
{
  "exp": "2022-02-22 07:35:57",
  "message": "Login success!",
  "status": 1,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDU0OTczNTcsImlhdCI6MTY0NTQzNzM1NywibmJmIjoxNjQ1NDM3MzU3LCJVSWQiOjZ9.0_d8tw1AZ_zTNrBxqTZbaxC9VYivBlvoM5ETN-yr1EQ",
  "user": {
    "AddInf1": "",
    "AddInf2": "",
    "AddInf3": "",
    "AddInf4": "",
    "AddInf5": "",
    "AddInf6": "",
    "CId": 1,
    "CreatedDate": "2020-12-22 18:24:07",
    "CreatedUId": 0,
    "DivId": 1,
    "EmpId": null,
    "FilePathM": "",
    "FilePathR": "",
    "FilePathS": "",
    "GCRecord": null,
    "Images": [],
    "ModifiedDate": "2021-12-24 18:30:22",
    "ModifiedUId": 0,
    "ResPriceGroupId": null,
    "RpAccId": null,
    "Rp_accs": [],
    "SyncDateTime": null,
    "UEmail": "fuckyou@gmial.com",
    "UFullName": "Administrator",
    "UGuid": "5a7cfb96-c0f8-413e-afa3-96d981ff5452",
    "UId": 6,
    "ULastActivityDate": "2021-12-24 18:31:36",
    "ULastActivityDevice": "Browser: chrome, Platform: linux, Details: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "UName": "admin",
    "URegNo": "asdfef2",
    "UShortName": "an",
    "UTypeId": 1,
    "User_type": {
      "CreatedDate": null,
      "CreatedUId": 0,
      "GCRecord": null,
      "ModifiedDate": "2020-10-27 17:34:42",
      "ModifiedUId": 6,
      "SyncDateTime": null,
      "UTypeDesc": "",
      "UTypeGuid": null,
      "UTypeId": 1,
      "UTypeName": "Administrator"
    }
  }
}
```

-----

## 2. Connect to ws

```url
ws://localhost:8080/ws/sms-register/
```

## 3. Send AUTH token POST

```json
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDU0OTczNTcsImlhdCI6MTY0NTQzNzM1NywibmJmIjoxNjQ1NDM3MzU3LCJVSWQiOjZ9.0_d8tw1AZ_zTNrBxqTZbaxC9VYivBlvoM5ETN-yr1EQ"}
```

