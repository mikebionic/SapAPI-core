# v1 api

## Optimized and updated code

### URL prefix: **/api/v1**

---

## Barcode api


| __Route__      | __Methods__ | __Status__ | __Note__            |
| -------------- | :---------: | :--------: | ------------------- |
| /v-barcodes/   |   **GET**   |   Active   | **@token required** |
| /tbl-barcodes/ |   **GET**   |   Active   | **@sha required**   |

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
| /v-rp-accs/   |   **GET**   |   Active   | **@token required** |
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
| /v-rp-accs/              |  **POST**   |   Active   | **@token required** |
| /api/tbl-dk-accs/        |  **POST**   |   Active   | **@sha required**   |
| /v-rp-accs/profile-edit/ |  **POST**   |   Active   | **@token required** |


[Example](./examples/rp_acc_v1.md)

---


## User api

> Get user info (by token and sha keys)

| __Route__          | __Methods__ | __Status__ | __Note__            |
| ------------------ | :---------: | :--------: | ------------------- |
| /api/v-users/      |   **GET**   |   Active   | **@token required** |
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

| __Route__            | __Methods__ | __Status__ | __Note__            |
| -------------------- | :---------: | :--------: | ------------------- |
| /api/v-devices/      |   **GET**   |   Active   | **@token required** |
| /api/tbl-dk-devices/ |   **GET**   |   Active   | **@sha required**   |

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


---

> Post device info or udpate if exists

| __Route__            | __Methods__ | __Status__ | __Note__          |
| -------------------- | :---------: | :--------: | ----------------- |
| /api/tbl-dk-devices/ |  **POST**   |   Active   | **@sha required** |

[Example](./examples/device_v1.md)

---


## Order inv api

> Checkout order invoice

| __Route__                 | __Methods__ | __Status__ | __Note__            |
| ------------------------- | :---------: | :--------: | ------------------- |
| /checkout-sale-order-inv/ |  **POST**   |   Active   | **@token required** |

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
| /v-order-invoices/ |   **GET**   |   Active   | **@token required** |

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
| /v-order-invoices/<Order_RegNo>/   |   **GET**   |   Active   | **@token required** |
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
| /order-payment-register-request/ |  **POST**   |   Active   | **@token required** |

[Example](./examples/order_payment_register_request.md)

---


> Validate order

| __Route__              | __Methods__ | __Status__ | __Note__            |
| ---------------------- | :---------: | :--------: | ------------------- |
| /order-inv-validation/ |  **POST**   |   Active   | **@token required** |

[Example](./examples/order_inv_validation.md)

---

> Paginate order invoices

| __Route__                   | __Methods__ | __Status__  | __Note__            |
| --------------------------- | :---------: | :---------: | ------------------- |
| /v-order-invoices/paginate/ |   **GET**   | Development | **@token required** |



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
| /gen-reg-no/ |  **POST**   |   Active   | **@token required** |

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
| __Name__     | __Type__ |
| ------------ | :------: |
| limit        | **int**  |
| showInactive | **int**  |



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
| /v-wishlist/ |   **GET**   |   Active   | **@token required**                        |
| /v-wishlist/ |  **POST**   |   Active   | **@token required**, provide ResId in body |
| /v-wishlist/ | **DELETE**  |   Active   | **@token required**, provide ResId in body |

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