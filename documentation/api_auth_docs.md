## Register api

| **Route**          | **Methods** | **Status** | **Note** |
| ------------------ | :---------: | :--------: | -------- |
| /register-request/ |   **GET**   |   Active   |

**Properties**
| **Name** | **Type** | **Description** | **Example**                 |
| -------- | :------: | --------------- | --------------------------- |
| type     | **str**  | --              | ?type=email or phone_number |

Header:
| **Title**   | **Type** | **Description**                     | **Example**         |
| ----------- | :------: | ----------------------------------- | ------------------- |
| Email       | **str**  | add if requests an email type       | example@example.com |
| PhoneNumber | **str**  | add if requests a phone_number type | +99361234567        |

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
---
