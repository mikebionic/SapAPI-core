# v1 api

## Optimized and updated code

### URL prefix: **/api/v1**

---

## Barcode api


| __Route__      | __Methods__ | __Status__ | __Note__          |
| -------------- | :---------: | :--------: | ----------------- |
| /v-barcodes/   |   **GET**   |   Active   |                   |
| /tbl-barcodes/ |   **GET**   |   Active   | **@sha required** |

**Properties**
| __Name__    | __Type__ | __Description__ | __Example__ |
| ----------- | :------: | --------------- | ----------- |
| id          | **int**  |
| barcodeGuid | **str**  |
| companyId   | **int**  |
| DivId       | **int**  |
| resourceId  | **int**  |
| unitId      | **int**  |
| barcodeVal  | **str**  |


---


## Rp_acc api


> Get Rp_acc info

| __Route__     | __Methods__ | __Status__ | __Note__            |
| ------------- | :---------: | :--------: | ------------------- |
| /v-rp-accs/   |   **GET**   |   Active   | **@token_required** |
| /tbl-rp-accs/ |   **GET**   |   Active   | **@sha required**   |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| regNo         |         **str**          |
| name          |         **str**          |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |
| DivGuid       |         **str**          |
| userId        |         **int**          |
| empId         |         **int**          |
| withImage     |         **int**          |




---

> Check rp_acc by provided json of data if it exists

| __Route__                | __Methods__ | __Status__ | __Note__ |
| ------------------------ | :---------: | :--------: | -------- |
| /check-rp-acc-existence/ |  **POST**   |   Active   |          |

[Example](./examples/rp_acc_existence_v1.md)

---

> Post user info or udpate if exists

| __Route__                | __Methods__ | __Status__ | __Note__            |
| ------------------------ | :---------: | :--------: | ------------------- |
| /v-rp-accs/              |  **POST**   |   Active   | **@token_required** |
| /api/tbl-dk-accs/        |  **POST**   |   Active   | **@sha required**   |
| /v-rp-accs/profile-edit/ |  **POST**   |   Active   | **@token_required** |


[Example](./examples/rp_acc_v1.md)

---

> Update avatar


| __Route__       | __Methods__ | __Status__ | __Note__            |
| --------------- | :---------: | :--------: | ------------------- |
| /update-avatar/ |  **POST**   |   Active   | **@token_required** |

**Properties**
| __Name__     | __Type__ | __Description__                                | __Example__ |
| ------------ | :------: | ---------------------------------------------- | ----------- |
| removeOthers | **int**  | Deletes old photographs from db and filesystem |

request.body = {
	"image": <image_file>
}

**response**
```py
{'ImgId': 76, 'ImgGuid': UUID('4c105a6a-4a94-4882-b82e-5b97806688c0'), 'EmpId': None, 'BrandId': None, 'CId': None, 'UId': None, 'RpAccId': 44, 'ResId': None, 'ResCatId': None, 'ProdId': None, 'FileName': '2b829e61a1269312f767d8e235e4.JPG', 'FilePath': '/ls/api/get-image/image/M/2b829e61a1269312f767d8e235e4.JPG', 'FilePathS': '/ls/api/get-image/image/S/2b829e61a1269312f767d8e235e4.JPG', 'FilePathM': '/ls/api/get-image/image/M/2b829e61a1269312f767d8e235e4.JPG', 'FilePathR': '/ls/api/get-image/image/R/2b829e61a1269312f767d8e235e4.JPG', 'FileHash': None, 'MinDarkFileName': '', 'MinDarkFilePath': '', 'MaxDarkFileName': '', 'MaxDarkFilePath': '', 'MinLightFileName': '', 'MinLightFilePath': '', 'MaxLightFileName': '', 'MaxLightFilePath': '', 'CreatedDate': '2022-04-19 18:19:02', 'ModifiedDate': '2022-04-19 18:19:02', 'SyncDateTime': '2022-04-19 18:19:02', 'CreatedUId': None, 'ModifiedUId': None, 'GCRecord': None}

```


----


## User api

> Get user info (by token and sha keys)

| __Route__          | __Methods__ | __Status__ | __Note__            |
| ------------------ | :---------: | :--------: | ------------------- |
| /api/v-users/      |   **GET**   |   Active   | **@token_required** |
| /api/tbl-dk-users/ |   **GET**   |   Active   | **@sha required**   |

**Properties**
| __Name__      |         __Type__         | __Description__              | __Example__ |
| ------------- | :----------------------: | ---------------------------- | ----------- |
| id            |         **int**          |
| regNo         |         **str**          |
| name          |         **str**          |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |
| withImage     |         **int**          | returns image FilePath props |


---

> Post user info or udpate if exists

| __Route__          | __Methods__ | __Status__ | __Note__          |
| ------------------ | :---------: | :--------: | ----------------- |
| /api/tbl-dk-users/ |  **POST**   |   Active   | **@sha required** |

[Example](./examples/user_v1.md)

---

## Device api


> Get user info (by token and sha keys)

| __Route__         | __Methods__ | __Status__ | __Note__            |
| ----------------- | :---------: | :--------: | ------------------- |
| /api/v-devices/   |   **GET**   |   Active   | **@token_required** |
| /api/tbl-devices/ |   **GET**   |   Active   | **@admin_required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| rpaccId       |         **int**          |
| userId        |         **int**          |
| isAllowed     |         **int**          |
| uniqueId      |         **str**          |
| name          |         **str**          |
| synchDateTime | **str repr of datetime** |

[Example](./examples/device_v1.md)

---

> Post device info or udpate if exists

| __Route__         | __Methods__ | __Status__ | __Note__          |
| ----------------- | :---------: | :--------: | ----------------- |
| /api/tbl-devices/ |  **POST**   |   Active   | **@sha required** |

[Example](./examples/device_v1.md)

---


## Order inv api

> Checkout order invoice

| __Route__                 | __Methods__ | __Status__ | __Note__            |
| ------------------------- | :---------: | :--------: | ------------------- |
| /checkout-sale-order-inv/ |  **POST**   |   Active   | **@token_required** |

[Example](./examples/checkout_order_inv_api.md)

---

> Get orders data

| __Route__            | __Methods__ | __Status__ | __Note__          |
| -------------------- | :---------: | :--------: | ----------------- |
| /tbl-order-invoices/ |   **GET**   |   Active   | **@sha required** |

**Properties**
| __Name__  |         __Type__         | __Description__ | __Example__ |
| --------- | :----------------------: | --------------- | ----------- |
| DivId     |         **int**          |
| notDivId  |         **int**          |
| stausId   |         **int**          |
| startDate | **str repr of datetime** |
| endDate   | **str repr of datetime** |
| currency  |         **str**          |

---

> Post orders from synchronizer

| __Route__            | __Methods__ | __Status__ | __Note__          |
| -------------------- | :---------: | :--------: | ----------------- |
| /tbl-order-invoices/ |  **POST**   |   Active   | **@sha required** |

---

> Get rp_acc's orders data

| __Route__          | __Methods__ | __Status__ | __Note__            |
| ------------------ | :---------: | :--------: | ------------------- |
| /v-order-invoices/ |   **GET**   |   Active   | **@token_required** |

**Properties**
| __Name__  |         __Type__         | __Description__ | __Example__ |
| --------- | :----------------------: | --------------- | ----------- |
| stausId   |         **int**          |
| startDate | **str repr of datetime** |
| endDate   | **str repr of datetime** |
| currency  |         **str**          |

---

> Get orders by reg no

| __Route__                          | __Methods__ | __Status__ | __Note__            |
| ---------------------------------- | :---------: | :--------: | ------------------- |
| /v-order-invoices/<Order_RegNo>/   |   **GET**   |   Active   | **@token_required** |
| /tbl-order-invoices/<Order_RegNo>/ |   **GET**   |   Active   | **@sha required**   |

**Properties**
| __Name__ | __Type__ | __Description__ | __Example__ |
| -------- | :------: | --------------- | ----------- |
| currency | **str**  |

---

> Request for order payment register
> This will return registered orderId and url that could be used for further payment

| __Route__                        | __Methods__ | __Status__ | __Note__            |
| -------------------------------- | :---------: | :--------: | ------------------- |
| /order-payment-register-request/ |  **POST**   |   Active   | **@token_required** |

[Example](./examples/order_payment_register_request.md)

---


> Validate order

| __Route__              | __Methods__ | __Status__ | __Note__            |
| ---------------------- | :---------: | :--------: | ------------------- |
| /order-inv-validation/ |  **POST**   |   Active   | **@token_required** |

[Example](./examples/order_inv_validation.md)

---

> Paginate order invoices

| __Route__                   | __Methods__ | __Status__  | __Note__            |
| --------------------------- | :---------: | :---------: | ------------------- |
| /v-order-invoices/paginate/ |   **GET**   | Development | **@token_required** |



---

## Payment info api


| __Route__                         | __Methods__ | __Status__ | __Note__                               |
| --------------------------------- | :---------: | :--------: | -------------------------------------- |
| /payment-validation-service-info/ |   **GET**   |   Active   | Gets info about online payment configs |

[Example](./examples/payment_api.md)

---

## RegNo api

> Generate pred reg no by provided json configs

| __Route__    | __Methods__ | __Status__ | __Note__            |
| ------------ | :---------: | :--------: | ------------------- |
| /gen-reg-no/ |  **POST**   |   Active   | **@token_required** |

[Example](./examples/reg_no_api.md)



---

## Session api

| __Route__                              | __Methods__ | __Status__ | __Note__ |
| -------------------------------------- | :---------: | :--------: | -------- |
| /set-session-currency/<currency_code>/ |   **GET**   |   Active   |
| /set-session-language/<language_code>/ |   **GET**   |   Active   |

---

## Image api

| __Route__  | __Methods__ | __Status__ | __Note__ |
| ---------- | :---------: | :--------: | -------- |
| /v-images/ |   **GET**   |   Active   |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |
| empId         |         **int**          |
| brandId       |         **int**          |
| companyId     |         **int**          |
| userId        |         **int**          |
| rpAccId       |         **int**          |
| resId         |         **int**          |
| categoryId    |         **int**          |
| prodId        |         **int**          |
| users         |         **int**          |
| brands        |         **int**          |
| resources     |         **int**          |
| rp_accs       |         **int**          |
| prods         |         **int**          |
| employees     |         **int**          |
| categories    |         **int**          |
| companies     |         **int**          |

**Headers example filtering** for excluding images by FileName and ImgGuid
**!! Warning !!** Payload can't be larger that 4Kb
```bash
curl 127.0.0.1:5000/ls/api/v1/v-images/ --header 'images-to-exclude: [{"FileName": "a6b8d0f70f31a320ded6937865d9.png", "ImgGuid": "d37ce4ba-45a6-49cb-838c-8ee6fd5b6815"}]'
```

---


| __Route__                   | __Methods__ | __Status__ | __Note__                                                                      |
| --------------------------- | :---------: | :--------: | ----------------------------------------------------------------------------- |
| /v-images-by-excluded-list/ |   **GET**   |   Active   | returns data without those that are provided in body json as on example below |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |
| empId         |         **int**          |
| brandId       |         **int**          |
| companyId     |         **int**          |
| userId        |         **int**          |
| rpAccId       |         **int**          |
| resId         |         **int**          |
| categoryId    |         **int**          |
| prodId        |         **int**          |
| users         |         **int**          |
| brands        |         **int**          |
| resources     |         **int**          |
| rp_accs       |         **int**          |
| prods         |         **int**          |
| employees     |         **int**          |
| categories    |         **int**          |
| companies     |         **int**          |

**Payload request data Example**
```json
[
	{
		"FileName": "a6b8d0f70f31a320ded6937865d9.png",
		"ImgGuid": "d37ce4ba-45a6-49cb-838c-8ee6fd5b6815"
	}
]
```

---

## Media api

| __Route__   | __Methods__ | __Status__ | __Note__ |
| ----------- | :---------: | :--------: | -------- |
| /tbl-media/ |   **GET**   |   Active   |

**Properties**
| __Name__   |         __Type__         | __Description__ | __Example__     |
| ---------- | :----------------------: | --------------- | --------------- |
| id         |         **int**          |
| title      |         **str**          |
| name       |         **str**          |
| body       |         **str**          |
| author     |         **str**          |
| isFeatured |         **int**          |
| categoryId |         **int**          |
| language   |         **str**          |                 | "tk_TM" "en_US" |
| startDate  | **str repr of datetime** |
| endDate    | **str repr of datetime** |

[Example](./examples/media_api.md)

---

## Translation api

| **Route**        |   **Methods**    | **Status** | **Note** |
| ---------------- | :--------------: | :--------: | -------- |
| /v-translations/ | **GET** **POST** |   Active   |

**Properties**
| **Name**   | **Type** | **Description** | **Example**     |
| ---------- | :------: | --------------- | --------------- |
| id         | **int**  |
| uuid       | **str**  |
| categoryId | **int**  |
| colorId    | **int**  |
| prodId     | **int**  |
| slImgId    | **int**  |
| langId     | **int**  |
| nameText   | **str**  |
| descText   | **str**  |
| language   | **str**  |                 | "tk_TM" "en_US" |

[Example](./examples/translation_api.md)

----


| **Route**            |   **Methods**    | **Status** | **Note** |
| -------------------- | :--------------: | :--------: | -------- |
| /v-res-translations/ | **GET** **POST** |   Active   |

**Properties**
| **Name**     | **Type** | **Description** | **Example**     |
| ------------ | :------: | --------------- | --------------- |
| id           | **int**  |
| uuid         | **str**  |
| resId        | **int**  |
| resName      | **str**  |
| resGuid      | **str**  |
| showResource | **int**  |
| nameText     | **str**  |
| descText     | **str**  |
| langId       | **int**  |
| language     | **str**  |                 | "tk_TM" "en_US" |

[Example](./examples/translation_api.md)

---



---

## Language api

| **Route**   | **Methods** | **Status** | **Note** |
| ----------- | :---------: | :--------: | -------- |
| /languages/ |   **GET**   |   Active   |

**Properties**
| **Name** | **Type** | **Description** | **Example**     |
| -------- | :------: | --------------- | --------------- |
| id       | **int**  |
| uuid     | **str**  |
| name     | **str**  |                 | "tk_TM" "en_US" |
| desc     | **str**  |

[Example](./examples/language_api.md)


## Discount resources

| **Route**            | **Methods** | **Status** | **Note** |
| -------------------- | :---------: | :--------: | -------- |
| /discount-resources/ |   **GET**   |   Active   |

**Properties**
| __Name__     | __Type__ | **Default** |
| ------------ | :------: | :---------: |
| limit        | **int**  |     15      |
| showInactive | **int**  |      0      |


## Ordered resources

| **Route**           | **Methods** | **Status** | **Note**                                         |
| ------------------- | :---------: | :--------: | ------------------------------------------------ |
| /ordered-resources/ |   **GET**   |   Active   | shows what else people buy with current resource |

**Properties**
| __Name__ | __Type__ | **Default** |      **Note**      |
| -------- | :------: | :---------: | :----------------: |
| id       | **int**  |             | ResId of a product |
| guid     | **str**  |             |      ResGuid       |
| limit    | **int**  |     15      |

[Example](./examples/resources_api.md)


## Recommended resources

| **Route**           | **Methods** | **Status** | **Note**                                 |
| ------------------- | :---------: | :--------: | ---------------------------------------- |
| /ordered-resources/ |   **GET**   |   Active   | **@token_required** shows recomendations |

**Properties**
| __Name__ | __Type__ | **Default** |
| -------- | :------: | :---------: |
| limit    | **int**  |     15      |

[Example](./examples/resources_api.md)

/recommended-resources/

----

<!-- !!!TODO: add filtering and currency showing if necessary -->


----

| __Route__        | __Methods__ | __Status__ | __Note__ |
| ---------------- | :---------: | :--------: | -------- |
| /res-collection/ |   **GET**   |   Active   |

**Properties**
| __Name__ | __Type__ |
| -------- | :------: |
| id       | **int**  |
| division | **int**  |
| company  | **int**  |
| name     | **str**  |
| uuid     | **str**  |

[Example](./examples/res_collections_api.md)


| __Route__    | __Methods__ | __Status__ | __Note__                                   |
| ------------ | :---------: | :--------: | ------------------------------------------ |
| /v-wishlist/ |   **GET**   |   Active   | **@token_required**                        |
| /v-wishlist/ |  **POST**   |   Active   | **@token_required**, provide ResId in body |
| /v-wishlist/ | **DELETE**  |   Active   | **@token_required**, provide ResId in body |

**Properties**
| __Name__ | __Type__ | __Description__                 | __Example__ |
| -------- | :------: | ------------------------------- | ----------- |
| page     | **int**  | returns next page of pagination |

[Example](./examples/wishlist_api.md)


---

## Rating Api

| __Route__   |     __Methods__      | __Status__ | __Note__            |
| ----------- | :------------------: | :--------: | ------------------- |
| /v-ratings/ | **POST**, **DELETE** |   Active   | **@token_required** |

[Example](./examples/rating_api.md)


----------------

## Statuses API


| __Route__      | __Methods__ | __Status__ | __Note__ |
| -------------- | :---------: | :--------: | -------- |
| /inv-statuses/ |   **GET**   |   Active   |
**Properties**
| __Name__ | __Type__ |
| -------- | :------: |
| id       | **int**  |
| uuid     | **str**  |
| name     | **str**  |
| name_tk  | **str**  |
| name_ru  | **str**  |
| name_en  | **str**  |

**request**

<prefix>/inv-statuses/?id=2

**response**

```json
{
  "data": [
    {
      "CreatedDate": null,
      "CreatedUId": 0,
      "GCRecord": null,
      "InvStatDesc_enUS": "Information received and being proceessed",
      "InvStatDesc_ruRU": "Информация получена и находится обработке",
      "InvStatDesc_tkTM": "Maglumat kabul edildi we degişli işler alnyp barylýar",
      "InvStatGuid": null,
      "InvStatId": 2,
      "InvStatName_enUS": "Received",
      "InvStatName_ruRU": "Принято",
      "InvStatName_tkTM": "Kabul edildi",
      "ModifiedDate": null,
      "ModifiedUId": 0,
      "SyncDateTime": null
    }
  ],
  "message": "Invoice statuses",
  "status": 1,
  "total": 1
}
```


-----


| __Route__  | __Methods__ | __Status__ | __Note__ |
| ---------- | :---------: | :--------: | -------- |
| /currency/ |   **GET**   |   Active   |
**Properties**
| __Name__ | __Type__ |
| -------- | :------: |
| id       | **int**  |
| uuid     | **str**  |
| name     | **str**  |
| name_tk  | **str**  |
| name_ru  | **str**  |
| name_en  | **str**  |

**request**

<prefix>/currency/?id=2

**response**

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
      "CreatedDate": null,
      "CreatedUId": 0,
      "CurrencyCode": "USD",
      "CurrencyDesc_enUS": "",
      "CurrencyDesc_ruRU": "",
      "CurrencyDesc_tkTM": "",
      "CurrencyGuid": "ba191a0e-fcec-4b83-a2c2-4ac24a4f786b",
      "CurrencyId": 2,
      "CurrencyName_enUS": "United states dollar",
      "CurrencyName_ruRU": "Доллар США",
      "CurrencyName_tkTM": "Amerikan dollary",
      "CurrencyNumCode": 840,
      "CurrencySymbol": "$",
      "GCRecord": null,
      "ModifiedDate": "2020-10-27 17:34:42",
      "ModifiedUId": 6,
      "SyncDateTime": null
    }
  ],
  "message": "Currencies",
  "status": 1,
  "total": 1
}
```

---

## Invoice API

>POST

| __Route__              |   __Methods__    | __Status__ | __Note__          |
| ---------------------- | :--------------: | :--------: | ----------------- |
| /api/v1/v-invoices/ | **POST** |   Active   | **@sha required** |

# example of request invoice

**request**
```json
[
    {
        "InvGuid": "582d5db3-3e58-4044-98e5-2f979b2960d8",
        "ModifiedDate": "2022-03-12T17:36:11.54"
    },
    {
        "InvGuid": "4a6f9c77-66a2-4902-91ae-d38badc1f001",
        "ModifiedDate": "2022-03-12T17:36:32.07"
    },
    {
        "InvGuid": "fa499e8c-b330-4c7b-8ae9-0d516f60caec",
        "ModifiedDate": "2022-03-12T17:37:23.827"
    },
    {
        "InvGuid": "6f06a7f5-eacf-4832-a2df-6bf84fa13041",
        "ModifiedDate": "2022-03-12T20:18:59.047"
    },
    {
        "InvGuid": "a1ec660a-7a7f-4a68-a530-401d5b99161b",
        "ModifiedDate": "2022-03-14T10:28:05.633"
    },
    {
        "InvGuid": "19edba3a-0c0d-444d-ba40-a5dbe7fba824",
        "ModifiedDate": "2022-03-15T12:53:47.75"
    }
]
```

**response**

```json
"data": [
		{
			"AddInf1": null,
			"AddInf10": null,
			"AddInf2": null,
			"AddInf3": null,
			"AddInf4": null,
			"AddInf5": null,
			"AddInf6": null,
			"AddInf7": null,
			"AddInf8": null,
			"AddInf9": null,
			"CGuid": null,
			"CId": null,
			"CreatedDate": "2022-04-26 18:47:18",
			"CreatedUId": 2013,
			"CurrencyCode": "TMT",
			"CurrencyId": 1,
			"CurrencySymbol": "m",
			"DivGuid": "e172dd11-07b4-4d3c-a9f8-58610df41f51",
			"DivId": 1,
			"EmpId": null,
			"GCRecord": null,
			"InvCreditDays": 0,
			"InvCreditDesc": null,
			"InvDate": "2022-04-26 18:38:27",
			"InvDesc": null,
			"InvDiscountAmount": 0.0,
			"InvExpenseAmount": 0.0,
			"InvFTotal": 300.0,
			"InvFTotalInWrite": "Üç yüz manat 0 teňňe",
			"InvGuid": "cddeea33-2a3c-471b-bf71-e637340cd5e9",
			"InvId": 14191,
			"InvLatitude": 0.0,
			"InvLongitude": 0.0,
			"InvModifyCount": 0,
			"InvPrintCount": 0,
			"InvRegNo": "SRHSF-00000054",
			"InvStatId": 1,
			"InvTaxAmount": 0.0,
			"InvTotal": 300.0,
			"InvTypeId": 3,
			"ModifiedDate": "2022-04-27 09:12:48",
			"ModifiedUId": 6,
			"PmId": null,
			"PtId": null,
			"RpAccGuid": "1e291363-9b33-416b-8443-9354f73f2f6b",
			"RpAccId": 567,
			"RpAccName": "Nagt satuw",
			"RpAccRegNo": "YP00000001",
			"Rp_acc": {
				"AddInf1": null,
				"AddInf10": "",
				"AddInf2": null,
				"AddInf3": null,
				"AddInf4": null,
				"AddInf5": null,
				"AddInf6": null,
				"AddInf7": "",
				"AddInf8": "",
				"AddInf9": "",
				"CId": 1,
				"CreatedDate": "2022-07-06 16:41:33",
				"CreatedUId": null,
				"DbGuid": null,
				"DeviceQty": null,
				"DivId": 1,
				"EmpId": null,
				"GCRecord": null,
				"GenderId": null,
				"IsMain": null,
				"ModifiedDate": "2022-07-07 17:08:30",
				"ModifiedUId": null,
				"NatId": null,
				"ReprId": null,
				"ResPriceGroupId": null,
				"RpAccAddress": null,
				"RpAccBirthDate": null,
				"RpAccEMail": null,
				"RpAccFirstName": null,
				"RpAccGuid": "1e291363-9b33-416b-8443-9354f73f2f6b",
				"RpAccHomePhoneNumber": null,
				"RpAccId": 567,
				"RpAccLangSkills": null,
				"RpAccLastActivityDate": "2022-07-06 16:41:33",
				"RpAccLastActivityDevice": null,
				"RpAccLastName": null,
				"RpAccLatitude": 0.0,
				"RpAccLongitude": 0.0,
				"RpAccMobilePhoneNumber": null,
				"RpAccName": "Nagt satuw",
				"RpAccPassportIssuePlace": null,
				"RpAccPassportNo": null,
				"RpAccPatronomic": null,
				"RpAccPurchBalanceLimit": 0.0,
				"RpAccRegNo": "YP00000001",
				"RpAccRegistrationPlace": "",
				"RpAccResidency": null,
				"RpAccSaleBalanceLimit": 0.0,
				"RpAccStatusId": 1,
				"RpAccTypeId": 2,
				"RpAccUName": "user178810",
				"RpAccViewCnt": null,
				"RpAccVisibleIndex": null,
				"RpAccWebAddress": null,
				"RpAccWorkFaxNumber": null,
				"RpAccWorkPhoneNumber": null,
				"RpAccZipCode": null,
				"SyncDateTime": "2022-07-06 16:41:33",
				"UnusedDeviceQty": null,
				"WpId": null
			},
			"SyncDateTime": "2022-07-29 18:18:31",
			"WhGuid": "6b0aa15f-00ff-4a40-9d52-a70e260067d6",
			"WhId": 1,
			"WpId": null,
			"inv_lines": [
				{
					"AddInf1": null,
					"AddInf10": null,
					"AddInf2": null,
					"AddInf3": null,
					"AddInf4": null,
					"AddInf5": null,
					"AddInf6": null,
					"AddInf7": null,
					"AddInf8": null,
					"AddInf9": null,
					"CreatedDate": "2022-07-29 18:18:31",
					"CreatedUId": null,
					"CurrencyCode": "TMT",
					"CurrencyId": 1,
					"CurrencySymbol": "m",
					"ExcRateValue": 0.0,
					"GCRecord": null,
					"InvId": 14191,
					"InvLineAmount": 1.0,
					"InvLineDate": "Wed, 27 Apr 2022 09:12:48 GMT",
					"InvLineDesc": null,
					"InvLineDiscAmount": 0.0,
					"InvLineExpenseAmount": 0.0,
					"InvLineFTotal": 19.2,
					"InvLineGuid": "7fef39cd-616f-44d4-8bec-fdbfb6ad134a",
					"InvLineId": 2585,
					"InvLinePrice": 19.2,
					"InvLineTaxAmount": 0.0,
					"InvLineTotal": 19.2,
					"LastVendorId": null,
					"ModifiedDate": "2022-07-29 18:18:31",
					"ModifiedUId": null,
					"ResGuid": "f639bd95-8b69-4276-84cf-6ca4fe7749c0",
					"ResId": 48,
					"ResName": "NIKAI - blender NB1700J  350W ",
					"ResRegNo": "YP00000046",
					"SyncDateTime": "2022-07-29 18:18:31",
					"UnitId": 1
				}
      ]
    }
]

```