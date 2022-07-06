
<host>/<prefix>/v1/v-ratings/

> POST, DELETE

**Request**
```json
[
	{
		"ResId": 17,
		"RtRatingValue": 4,
		"RtRemark": "It is good, but has small disadvantages!"
	}
]
```

**Response**
```json
{
  "data": [
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CId": null,
      "CreatedDate": null,
      "CreatedUId": null,
      "DivId": null,
      "EmpId": null,
      "GCRecord": null,
      "ModifiedDate": null,
      "ModifiedUId": null,
      "ResId": 17,
      "RpAccId": 44,
      "RtGuid": "9f59071d-f531-44d1-b9b5-48a5d14e1be0",
      "RtId": null,
      "RtRatingValue": 4,
      "RtRemark": "It is good, but has small disadvantages!",
      "RtValidated": false,
      "SyncDateTime": null,
      "UId": null,
      "message": "Rating created!",
      "status": 1
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 1
}
```
