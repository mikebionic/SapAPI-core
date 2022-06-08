## Post device data

> /v1/tbl-devices/

**Request**

```json
[
	{
		"AddInf1": "",
		"AddInf2": "",
		"AddInf3": "",
		"AddInf4": "hello",
		"AddInf5": "",
		"AddInf6": "1111111,androidId=e4d788879fbe6635,baseOS=,release=10,brand=samsung,device=a7y18lte,display=QP1A.190711.020.A750FXXU5CUI4,manufacturer=samsung,model=SM-A750F,isPhysicalDevice=true",
		"AllowedDate": null,
		"CreatedDate": "2022-01-29 08:00:04",
		"CreatedUId": null,
		"DevDesc": null,
		"DevGuid": "ace9103d-9d83-4a72-8c0f-effb341b3c44",
		"DevId": 62,
		"DevName": "Dowlpack",
		"DevUniqueId": "e4d788879fbe6635",
		"DevVerifyDate": null,
		"DevVerifyKey": null,
		"DisallowedDate": null,
		"GCRecord": null,
		"IsAllowed": true,
		"ModifiedDate": "2022-01-29 08:00:04",
		"ModifiedUId": null,
		"RpAccId": null,
		"SyncDateTime": "2022-01-29 08:00:04",
		"UFullName": null,
		"UId": 10,
		"UName": "dowlpack"
	}
]
```

**Response**

```json
{
  "data": [
    {
      "AddInf1": "",
      "AddInf2": "",
      "AddInf3": "",
      "AddInf4": "hello",
      "AddInf5": "",
      "AddInf6": "1111111,androidId=e4d788879fbe6635,baseOS=,release=10,brand=samsung,device=a7y18lte,display=QP1A.190711.020.A750FXXU5CUI4,manufacturer=samsung,model=SM-A750F,isPhysicalDevice=true",
      "AllowedDate": null,
      "CreatedDate": "2022-01-29 08:00:04",
      "CreatedUId": null,
      "DevDesc": null,
      "DevGuid": "ace9103d-9d83-4a72-8c0f-effb341b3c44",
      "DevId": 62,
      "DevName": "Dowlpack",
      "DevUniqueId": "e4d788879fbe6635",
      "DevVerifyDate": null,
      "DevVerifyKey": null,
      "DisallowedDate": null,
      "GCRecord": null,
      "IsAllowed": true,
      "ModifiedDate": "2022-01-29 08:00:04",
      "ModifiedUId": null,
      "RpAccId": null,
      "SyncDateTime": "2022-01-29 08:00:04",
      "UFullName": null,
      "UId": 10,
      "UName": "dowlpack"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 1
}
```


-------------

## Get device data

> /v1/v-devices/

> /v1/tbl-devices/ 

**response**
```json
{
  "data": [
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": "id=QP1A.190711.020,androidId=e4d788879fbe6635,baseOS=,release=10,brand=samsung,device=a7y18lte,display=QP1A.190711.020.A750FXXU5CTK1,manufacturer=samsung,model=SM-A750F,isPhysicalDevice=true",
      "AllowedDate": null,
      "CreatedDate": "2021-02-15 18:04:07",
      "CreatedUId": null,
      "DevDesc": null,
      "DevGuid": "53fca8ad-28a8-4b5f-af48-9a29be7274b5",
      "DevId": 6,
      "DevName": "2021-01-14 23:44:26.778464",
      "DevUniqueId": "mike1",
      "DevVerifyDate": "2021-02-15 22:39:32",
      "DevVerifyKey": "gAAAAABgKrHV_yXWeWXC0D7q1GuUy6h5M9venXeUwVWnFqS3Uf209nKOTXNurZRgMXznaWIjzSLWLR_Pf_P9tq2KFWvPx2gWtxUF4X7H1f850oPiGi1feXt5eI3Eqe86v5sNdbBVhe7_IzZ00q7l205A1g31dYn9_XzkSikNIHjaC0hYuiYXDS7tG7_ZO7XTfIdc8ajX4iFq23m4i3oiCAxxWyCs4ieT-qMXgy4l8hY9YLEZwnQBgGWTz-j1rqCjZANmAI82ai5FNGeDTMPPCizK2Ve3alz1LkXjjaaeJt9TxZDuZGWWN6rNZw0ARU80FVy3QsItip5R6_a6VNKMVIa35RY7ECypjgpG0Q_AmaYlc6EGXRT3hCqOsA1Ta0uacKMntgE_0npJcdsVJEjH7mznfn_Y1c6hT4rqaunYHFMLnD8KTPIQsypfhIcykT4wtMqi7p6b3gKSszRKJMztk5Lk6KimYiv7l5UM9apSTFWggY63TudSljyI1rmi_8ED2AcO26f38r5YZovQfgmHe5I72eVAZPRtj609T0ZOBr2n4cry9FGuk5871BLW06wo9IPcZvkMsU6RoYmYDAD2kmiCbAnZZGgP53qJOjfqsYRwrAchH_vlllHi1q7LHRw7PYEN2R3L4xgizIQ7qD8sept3DhNJ09YRoQ==",
      "DisallowedDate": null,
      "GCRecord": null,
      "IsAllowed": true,
      "ModifiedDate": "2021-02-15 22:38:10",
      "ModifiedUId": null,
      "RpAccId": null,
      "SyncDateTime": "2021-02-15 18:04:07",
      "UFullName": "Mike Bionic",
      "UId": 3,
      "UName": "administrator"
    },
  ],
  "message": "Device",
  "status": 1,
  "total": 1
}
```