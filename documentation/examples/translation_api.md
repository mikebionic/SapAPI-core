Translation Api

**Request**

> POST

http://<url>/<prefix>/v1/v-translations/

```json
[
	{
		"TranslName": "Кофеварка",
		"LangName": "ru",
		"ResCatName": "Kofe",
		"TranslDesc": "Используются для изгтовленгя кофе"
	},
	{
		"TranslName": "Peripherals",
		"LangName": "en",
		"ResCatName": "perife",
		"TranslDesc": "a devised used for computer tah attached"
	},
	{
		"TranslName": "Watches",
		"LangName": "en",
		"ResCatName": "saga",
		"TranslDesc": "Clock devices"
	}
]
```

**Response**

```json
{
  "data": [
    {
      "LangName": "ru",
      "ResCatName": "Kofe",
      "TranslDesc": "Используются для изгтовленгя кофе",
      "TranslName": "Кофеварка"
    },
    {
      "LangName": "en",
      "ResCatName": "perife",
      "TranslDesc": "a devised used for computer tah attached",
      "TranslName": "Peripherals"
    },
    {
      "LangName": "en",
      "ResCatName": "saga",
      "TranslDesc": "Clock devices",
      "TranslName": "Watches"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 3
}
```
---

> GET

http://<url>/<prefix>/v1/v-translations/?language=en

**Response**

```json
{
  "data": [
    {
      "AddInf1": "",
      "AddInf2": "",
      "AddInf3": "",
      "AddInf4": "",
      "AddInf5": "",
      "AddInf6": "",
      "ColorId": null,
      "CreatedDate": "2022-02-10 15:08:00",
      "CreatedUId": 0,
      "GCRecord": null,
      "LangId": 3,
      "LangName": "en-US",
      "ResCatName": "Sagatlar",
      "ModifiedDate": "2022-02-10 16:02:51",
      "ModifiedUId": 0,
      "ProdId": null,
      "ResCatId": 3,
      "SlImgId": null,
      "SyncDateTime": null,
      "TranslDesc": "Clock devices",
      "TranslGuid": "28ab309b-402a-49a7-928c-eb687e140676",
      "TranslId": 1,
      "TranslName": "Watches"
    }
  ],
  "message": "Translation",
  "status": 1,
  "total": 1
}
```


-----
Res_translation API


> POST

http://<url>/<prefix>/v1/v-translations/

**request**

```json
[
	{
		"ResName": "Haryt",
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "Bi Mand Watches",
		"ResDesc": "New updated watches",
		"LangName": "en"		
	},
	{
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "Bi mand taze sagatlar!",
		"ResDesc": "Taze we dowrebap sagatlar",
		"LangName": "tk"		
	},
	{
		"ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
		"ResName": "часы Bi mand!",
		"ResDesc": "Современные часы с новым функционалом",
		"LangName": "ru"		
	}
]
```
> GET

/v1/v-res-translations/?showResource=1

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
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 3,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "New updated watches",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi Mand Watches",
      "ResTranslGuid": "ae1b75e8-9f2a-47d2-94a0-7b87ab1d839f",
      "ResTranslId": 4,
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 1,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Taze we dowrebap sagatlar",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi mand taze sagatlar!",
      "ResTranslGuid": "36a9ce5b-7af8-459d-8f91-952967f48452",
      "ResTranslId": 5,
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 2,
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Современные часы с новым функционалом",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "часы Bi mand!",
      "ResTranslGuid": "2d9be9c2-43c0-47a0-86b6-021fb21975c1",
      "ResTranslId": 6,
      "SyncDateTime": "2022-03-31 16:24:52"
    }
  ],
  "fail_total": 0,
  "fails": [],
  "message": "Success",
  "status": 1,
  "success_total": 3
}
```


-----
Get 


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
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 2,
      "LangName": "ru-RU",
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Современные часы с новым функционалом",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "часы Bi mand!",
      "ResTranslGuid": "2d9be9c2-43c0-47a0-86b6-021fb21975c1",
      "ResTranslId": 6,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Sagatlar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 3,
        "ResDesc": "Bu sagartoran gowy Renk: gara, Operasion Ulgam: android, black material",
        "ResFullDesc": null,
        "ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
        "ResHeight": 0.0,
        "ResId": 28,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Bi Mand 3",
        "ResRegNo": "AN00000036",
        "ResTypeId": null,
        "ResViewCnt": 1244554,
        "ResVisibleIndex": 8,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 1,
      "LangName": "tk-TM",
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "Taze we dowrebap sagatlar",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi mand taze sagatlar!",
      "ResTranslGuid": "36a9ce5b-7af8-459d-8f91-952967f48452",
      "ResTranslId": 5,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Sagatlar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 3,
        "ResDesc": "Bu sagartoran gowy Renk: gara, Operasion Ulgam: android, black material",
        "ResFullDesc": null,
        "ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
        "ResHeight": 0.0,
        "ResId": 28,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Bi Mand 3",
        "ResRegNo": "AN00000036",
        "ResTypeId": null,
        "ResViewCnt": 1244554,
        "ResVisibleIndex": 8,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": null,
      "AddInf2": null,
      "AddInf3": null,
      "AddInf4": null,
      "AddInf5": null,
      "AddInf6": null,
      "CreatedDate": "2022-03-31 16:24:52",
      "CreatedUId": null,
      "GCRecord": null,
      "LangId": 3,
      "LangName": "en-US",
      "ModifiedDate": "2022-03-31 16:24:52",
      "ModifiedUId": null,
      "ResDesc": "New updated watches",
      "ResFullDesc": null,
      "ResId": 28,
      "ResName": "Bi Mand Watches",
      "ResTranslGuid": "ae1b75e8-9f2a-47d2-94a0-7b87ab1d839f",
      "ResTranslId": 4,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Sagatlar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 3,
        "ResDesc": "Bu sagartoran gowy Renk: gara, Operasion Ulgam: android, black material",
        "ResFullDesc": null,
        "ResGuid": "6c072a49-cb38-42fe-90b3-8ef185eb892d",
        "ResHeight": 0.0,
        "ResId": 28,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Bi Mand 3",
        "ResRegNo": "AN00000036",
        "ResTypeId": null,
        "ResViewCnt": 1244554,
        "ResVisibleIndex": 8,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": "2022-03-31 16:24:52"
    },
    {
      "AddInf1": "",
      "AddInf2": "",
      "AddInf3": "",
      "AddInf4": "",
      "AddInf5": "",
      "AddInf6": "",
      "CreatedDate": "2021-07-09 16:10:08",
      "CreatedUId": 0,
      "GCRecord": null,
      "LangId": 2,
      "LangName": "ru-RU",
      "ModifiedDate": "2021-07-09 16:10:08",
      "ModifiedUId": 0,
      "ResDesc": "Похоже что подольше",
      "ResFullDesc": "Подольшеееееееееее обзяснение",
      "ResId": 12,
      "ResName": "Хрень какая то но на русском",
      "ResTranslGuid": null,
      "ResTranslId": 3,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Kameralar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 6,
        "ResDesc": "Sony Camera MxP model 2, 512 MbPx, Big lenses, Great ligtht, Garankylykda syomka ukyply, Renki: Gara",
        "ResFullDesc": null,
        "ResGuid": "b0993666-00f4-4d88-af06-ce3012c9caa9",
        "ResHeight": 0.0,
        "ResId": 12,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Sony MxP 2",
        "ResRegNo": "AN00000015",
        "ResTypeId": null,
        "ResViewCnt": 0,
        "ResVisibleIndex": 5,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": null
    },
    {
      "AddInf1": "",
      "AddInf2": "",
      "AddInf3": "",
      "AddInf4": "",
      "AddInf5": "",
      "AddInf6": "",
      "CreatedDate": "2021-07-09 16:08:39",
      "CreatedUId": 0,
      "GCRecord": null,
      "LangId": 1,
      "LangName": "tk-TM",
      "ModifiedDate": "2021-07-09 16:08:39",
      "ModifiedUId": 0,
      "ResDesc": "Onun Dushundirishi",
      "ResFullDesc": "We fucking doly dushundirishi",
      "ResId": 12,
      "ResName": "Super bet haryt Turkmence",
      "ResTranslGuid": null,
      "ResTranslId": 2,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Kameralar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 6,
        "ResDesc": "Sony Camera MxP model 2, 512 MbPx, Big lenses, Great ligtht, Garankylykda syomka ukyply, Renki: Gara",
        "ResFullDesc": null,
        "ResGuid": "b0993666-00f4-4d88-af06-ce3012c9caa9",
        "ResHeight": 0.0,
        "ResId": 12,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Sony MxP 2",
        "ResRegNo": "AN00000015",
        "ResTypeId": null,
        "ResViewCnt": 0,
        "ResVisibleIndex": 5,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": null
    },
    {
      "AddInf1": "",
      "AddInf2": "",
      "AddInf3": "",
      "AddInf4": "",
      "AddInf5": "",
      "AddInf6": "",
      "CreatedDate": "2021-07-09 16:06:41",
      "CreatedUId": 0,
      "GCRecord": null,
      "LangId": 3,
      "LangName": "en-US",
      "ModifiedDate": "2021-07-09 16:06:41",
      "ModifiedUId": 0,
      "ResDesc": "Translated Description",
      "ResFullDesc": "Translated Full Descrtiption",
      "ResId": 12,
      "ResName": "Translated name",
      "ResTranslGuid": null,
      "ResTranslId": 1,
      "Resource": {
        "AddInf1": null,
        "AddInf2": "Kameralar",
        "AddInf3": null,
        "AddInf4": null,
        "AddInf5": null,
        "AddInf6": null,
        "BrandId": null,
        "CId": 1,
        "CreatedDate": "2020-10-27 17:39:11",
        "CreatedUId": null,
        "DivId": 1,
        "GCRecord": null,
        "IsMain": null,
        "ModifiedDate": "2020-10-27 17:49:15",
        "ModifiedUId": null,
        "ResCatId": 6,
        "ResDesc": "Sony Camera MxP model 2, 512 MbPx, Big lenses, Great ligtht, Garankylykda syomka ukyply, Renki: Gara",
        "ResFullDesc": null,
        "ResGuid": "b0993666-00f4-4d88-af06-ce3012c9caa9",
        "ResHeight": 0.0,
        "ResId": 12,
        "ResLastVendorId": null,
        "ResLength": 0.0,
        "ResMainImgId": 0,
        "ResMakerId": null,
        "ResMaxSaleAmount": 0.0,
        "ResMaxSalePrice": 0.0,
        "ResMinSaleAmount": 0.0,
        "ResMinSalePrice": 0.0,
        "ResName": "Sony MxP 2",
        "ResRegNo": "AN00000015",
        "ResTypeId": null,
        "ResViewCnt": 0,
        "ResVisibleIndex": 5,
        "ResWeight": 0.0,
        "ResWidth": 0.0,
        "SyncDateTime": "2020-10-27 17:39:11",
        "UnitId": 1,
        "UsageStatusId": 1
      },
      "SyncDateTime": null
    }
  ],
  "message": "Translation",
  "status": 1,
  "total": 6
}
```