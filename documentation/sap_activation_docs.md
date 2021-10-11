| URL          |  method  | description                                                                                    |
| ------------ | :------: | ---------------------------------------------------------------------------------------------- |
| /devices/mobile-sync/ | **POST** | update and add devices for specific company and return the result of insertions and activation |

/sap/api/activation/devices/mobile-sync/

```json
json_data = {
	"DbInfGuid": company.DbInfGuid, //! CGuid hem bolar.
	// ... other company info
	"Devices": [
		{
			"DevId": DevId,
			"DevGuid": DevGuid, //!
			"DevUniqueId": DevUniqueId, //!
			"RpAccId": RpAccId,
			"DevName": DevName,
			"DevDesc": DevDesc,
			"IsAllowed": IsAllowed, //!
			"DevVerifyDate": DevVerifyDate, //!
			"DevVerifyKey": DevVerifyKey, //!
			"AddInf1": AddInf1,
			"AddInf2": AddInf2,
			"AddInf3": AddInf3,
			"AddInf4": AddInf4,
			"AddInf5": AddInf5,
			"AddInf6": AddInf6,
			"CreatedDate": CreatedDate,
			"ModifiedDate": ModifiedDate,
			"SyncDateTime": SyncDateTime,
			"CreatedUId": CreatedUId,
			"ModifiedUId": ModifiedUId,
			"GCRecord": GCRecord
		},
		// ... other devices
	]
}
```

---

Response should be inserted to Local DB if not empty.
+ apply cryptography to validate phone activation.

While response processed, client side goes through device list and find it's device's DevUniqueId and validate it's register state.
If not registered, contact SapCozgut company and after activation make another similar request.

```json
{
	"status": 1,
	"data": {
		"DbGuid": DbGuid,
		"DeviceQty": allowed_device_qty,
		"UnusedDeviceQty": unused_device_qty,
		"Devices": [
			{
				"DevId": DevId,
				"DevGuid": DevGuid,
				"DevUniqueId": DevUniqueId,
				"RpAccId": RpAccId,
				"DevName": DevName,
				"DevDesc": DevDesc,
				"IsAllowed": IsAllowed, // This is important
				"DevVerifyDate": DevVerifyDate, // generate Yours
				"DevVerifyKey": DevVerifyKey,
				"AddInf1": AddInf1,
				"AddInf2": AddInf2,
				"AddInf3": AddInf3,
				"AddInf4": AddInf4,
				"AddInf5": AddInf5,
				"AddInf6": AddInf6,
				"CreatedDate": CreatedDate,
				"ModifiedDate": ModifiedDate,
				"SyncDateTime": SyncDateTime,
				"CreatedUId": CreatedUId,
				"ModifiedUId": ModifiedUId,
				"GCRecord": GCRecord
			},
			// ...
		]
	},
	"message": "Device mobile sync",
	"total": 1
}
```