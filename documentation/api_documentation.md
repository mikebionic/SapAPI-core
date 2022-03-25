# Welcome to Sap Api documentation!
This documentation provides an info about routes and their usage, use it for building client-side applications.


## Legend
| Shortcut            | Description                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------------- |
| **!!**              | Warning sign                                                                                                |
| **!!deprecated**    | Route might be updated to different route and will be deleted after a major update process and verification |
| **@sha required**   | Requires api key of **Synchronizer** for **@sha required**                                                  |
| **@token required** | **@token required** of **Rp acc** login                                                                     |
---


## Authentication API
Provide **username** and **password** in Authentication headers

| __Route__   | __Methods__ | __Status__ | __Note__ |
| ----------- | :---------: | :--------: | -------- |
| /api/login/ |   **GET**   |  Updated   |

**Properties**
| __Name__ | __Type__ | __Description__                                                      | __Example__          |
| -------- | :------: | -------------------------------------------------------------------- | -------------------- |
| type     | **str**  | validates the User model of tables depending on type (default: User) | user, rp_acc, device |

---

| __Route__           | __Methods__ | __Status__ | __Note__         |
| ------------------- | :---------: | :--------: | ---------------- |
| /api/login/users/   |   **GET**   |   Active   | **!!deprecated** |
| /api/login/rp-accs/ |   **GET**   |   Active   | **!!deprecated** |

---


## Fetch information API

| __Route__          | __Methods__ | __Status__ | __Note__                         |
| ------------------ | :---------: | :--------: | -------------------------------- |
| /api/api-config/   |   **GET**   |   Active   | API config information           |
| /api/company-info/ |   **GET**   |   Active   | Company and Division information |


---


## Synchronizing, data queries and insertions API



| __Route__             |   __Methods__    | __Status__ | __Note__          |
| --------------------- | :--------------: | :--------: | ----------------- |
| /api/tbl-dk-barcodes/ | **GET** **POST** |  Updated   | **@sha required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| val           |         **str**          |
| synchDateTime | **str repr of datetime** |
| DivId         |         **int**          |
| notDivId      |         **int**          |


---

| __Route__       | __Methods__ | __Status__ | __Note__            |
| --------------- | :---------: | :--------: | ------------------- |
| /api/v-company/ |   **GET**   |   Active   | **@token required** |


| __Route__     |   __Methods__    | __Status__ | __Note__          |
| ------------- | :--------------: | :--------: | ----------------- |
| /api/company/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__ | __Type__ | __Description__ | __Example__ |
| -------- | :------: | --------------- | ----------- |
| CGuid    | **str**  |

---

| __Route__      |   __Methods__    | __Status__ | __Note__          |
| -------------- | :--------------: | :--------: | ----------------- |
| /api/division/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__ | __Type__ | __Description__ | __Example__ |
| -------- | :------: | --------------- | ----------- |
| DivGuid  | **str**  |

---

| __Route__              |   __Methods__    | __Status__  | __Note__          |
| ---------------------- | :--------------: | :---------: | ----------------- |
| /api/tbl-dk-exc-rates/ | **GET** **POST** | Development | **@sha required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| currencyId    |         **int**          |
| synchDateTime | **str repr of datetime** |
| excRateDate   | **str repr of datetime** |


---

| __Route__           |   __Methods__    | __Status__ | __Note__            |
| ------------------- | :--------------: | :--------: | ------------------- |
| /api/tbl-dk-images/ | **GET** **POST** |   Active   | **@sha required**   |
| /api/v-images/      |     **GET**      |   Active   | **@token required** |

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


---

| __Route__                    | __Methods__ | __Status__ | __Note__ |
| ---------------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-payment-methods/ |   **GET**   |   Active   |
| /api/tbl-dk-payment-types/   |   **GET**   |   Active   |


---

| __Route__               |   __Methods__    | __Status__ | __Note__          |
| ----------------------- | :--------------: | :--------: | ----------------- |
| /api/tbl-dk-res-prices/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__   | __Type__ | __Description__ | __Example__ |
| ---------- | :------: | --------------- | ----------- |
| DivId      | **int**  |
| notDivId   | **int**  |
| priceType  | **int**  |
| priceGroup | **int**  |


---

| __Route__          | __Methods__ | __Status__ | __Note__            |
| ------------------ | :---------: | :--------: | ------------------- |
| /api/v-res-prices/ |   **GET**   |   Active   | **@token required** |

**Properties**
| __Name__  | __Type__ | __Description__ | __Example__ |
| --------- | :------: | --------------- | ----------- |
| DivId     | **int**  |
| notDivId  | **int**  |
| priceType | **int**  |


---

| __Route__                | __Methods__ | __Status__ | __Note__            |
| ------------------------ | :---------: | :--------: | ------------------- |
| /api/v-res-price-groups/ |   **GET**   |   Active   | **@token required** |

**Properties**
| __Name__      | __Type__ | __Description__ | __Example__ |
| ------------- | :------: | --------------- | ----------- |
| id            | **int**  |
| usageStatus   | **int**  |
| name          | **str**  |
| fromPriceType | **int**  |
| toPriceType   | **int**  |


---

| __Route__               |   __Methods__    | __Status__ | __Note__            |
| ----------------------- | :--------------: | :--------: | ------------------- |
| /api/tbl-dk-res-totals/ | **GET** **POST** |   Active   | **@sha required**   |
| /api/v-res-totals/      |     **GET**      |   Active   | **@token required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |


---


| __Route__           | __Methods__ | __Status__ | __Note__ |
| ------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-brands/ |   **GET**   |   Active   |

**Properties**
| __Name__  | __Type__ | __Description__                  | __Example__ |
| --------- | :------: | -------------------------------- | ----------- |
| id        | **int**  |
| name      | **str**  |
| imageList | **int**  | returns Image[] list in response |


---
## Category API

| __Route__               | __Methods__ | __Status__ | __Note__ |
| ----------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-categories/ |   **GET**   |   Active   |

**Properties**
| __Name__        | __Type__ | __Description__ | __Example__ |
| --------------- | :------: | --------------- | ----------- |
| DivId           | **int**  |
| notDivId        | **int**  |
| avoidQtyCheckup | **int**  |


---

| __Route__               | __Methods__ | __Status__ | __Note__ |
| ----------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-categories/ |  **POST**   |   Active   |


---

| __Route__                        | __Methods__ | __Status__  | __Note__ |
| -------------------------------- | :---------: | :---------: | -------- |
| /api/tbl-dk-categories/paginate/ |   **GET**   | Development |

**Properties**
| __Name__ | __Type__ | __Description__ | __Example__ |
| -------- | :------: | --------------- | ----------- |
| page     | **int**  |


---

## Resource API


| __Route__              |   __Methods__    | __Status__ | __Note__          |
| ---------------------- | :--------------: | :--------: | ----------------- |
| /api/tbl-dk-resources/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |
| id            |         **int**          |
| regNo         |         **str**          |
| name          |         **str**          |


---

| __Route__         | __Methods__ | __Status__ | __Note__ |
| ----------------- | :---------: | :--------: | -------- |
| /api/v-resources/ |   **GET**   |   Active   |

**Properties**
| __Name__        | __Type__ | __Description__     | __Example__ |
| --------------- | :------: | ------------------- | ----------- |
| DivId           | **int**  |
| notDivId        | **int**  |
| avoidQtyCheckup | **int**  |
| showMain        | **int**  | shows featured only |


---

| __Route__             | __Methods__ | __Status__ | __Note__         |
| --------------------- | :---------: | :--------: | ---------------- |
| /api/v-resources/:id/ |   **GET**   |   Active   | **!!deprecated** |

**Properties**
| __Name__    | __Type__ | __Description__                | __Example__ |
| ----------- | :------: | ------------------------------ | ----------- |
| showRelated | **int**  | shows "Related_resources" list |
| showRatings | **int**  | shows "Rating" list            |


---

| __Route__              | __Methods__ | __Status__ | __Note__         |
| ---------------------- | :---------: | :--------: | ---------------- |
| /api/v-full-resources/ |   **GET**   |  Old ver   | **!!deprecated** |

**Properties**
| __Name__ | __Type__ | __Description__     | __Example__ |
| -------- | :------: | ------------------- | ----------- |
| DivId    | **int**  |
| notDivId | **int**  |
| showMain | **int**  | shows featured only |

---

| __Route__                               | __Methods__ | __Status__ | __Note__ |
| --------------------------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-categories/:id/v-resources/ |   **GET**   |  Old ver   |

**Properties**
| __Name__        | __Type__ | __Description__ | __Example__ |
| --------------- | :------: | --------------- | ----------- |
| DivId           | **int**  |
| notDivId        | **int**  |
| avoidQtyCheckup | **int**  |


---

| __Route__       | __Methods__ | __Status__ | __Note__ |
| --------------- | :---------: | :--------: | -------- |
| /api/resources/ |   **GET**   |   Active   |

**Properties**
| __Name__   | __Type__ | __Description__     | __Example__ |
| ---------- | :------: | ------------------- | ----------- |
| page       | **int**  |
| sort       | **str**  |
| per_page   | **int**  |
| category   | **int**  |
| brand      | **int**  |
| from_price | **int**  |
| to_price   | **int**  |
| DivId      | **int**  |
| notDivId   | **int**  |
| showMain   | **int**  | shows featured only |
| limit      | **int**  |
| search     | **str**  |

---

| __Route__            |   __Methods__    |           __Status__           | __Note__            |
| -------------------- | :--------------: | :----------------------------: | ------------------- |
| /api/v-rp-accs/      |     **GET**      | **!!deprecated** (use v1 api)  | **@token required** |
| /api/tbl-dk-rp-accs/ | **GET** **POST** | **!!deprecated**  (use v1 api) | **@sha required**   |

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

---

| __Route__                        |   __Methods__    | __Status__ | __Note__          |
| -------------------------------- | :--------------: | :--------: | ----------------- |
| /api/tbl-dk-rp-acc-trans-totals/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |


---

| __Route__            | __Methods__ | __Status__ | __Note__ |
| -------------------- | :---------: | :--------: | -------- |
| /api/tbl-dk-sliders/ |   **GET**   |   Active   |

**Properties**
| __Name__ | __Type__ | __Description__ | __Example__ |
| -------- | :------: | --------------- | ----------- |
| DivId    | **int**  |
| notDivId | **int**  |
| id       | **int**  |
| name     | **str**  |


---

| __Route__                  | __Methods__ | __Status__ | __Note__         |
| -------------------------- | :---------: | :--------: | ---------------- |
| /api/tbl-dk-sliders/:name/ |   **GET**   |   Active   | **!!deprecated** |


---


| __Route__         | __Methods__ | __Status__ | __Note__            |
| ----------------- | :---------: | :--------: | ------------------- |
| /api/device-user/ |   **GET**   |   Active   | **@token required** |


---


| __Route__          |   __Methods__    | __Status__ | __Note__            |
| ------------------ | :--------------: | :--------: | ------------------- |
| /api/v-users/      |     **GET**      |   Active   | **@token required** |
| /api/tbl-dk-users/ | **GET** **POST** |   Active   | **@sha required**   |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| regNo         |         **str**          |
| name          |         **str**          |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |

---


| __Route__               |   __Methods__    | __Status__ | __Note__            |
| ----------------------- | :--------------: | :--------: | ------------------- |
| /api/v-warehouses/      |     **GET**      |   Active   | **@token required** |
| /api/tbl-dk-warehouses/ | **GET** **POST** |   Active   | **@sha required**   |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| name          |         **str**          |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |

---


| __Route__                 |   __Methods__    | __Status__ | __Note__          |
| ------------------------- | :--------------: | :--------: | ----------------- |
| /api/tbl-dk-work-periods/ | **GET** **POST** |   Active   | **@sha required** |

**Properties**
| __Name__      |         __Type__         | __Description__ | __Example__ |
| ------------- | :----------------------: | --------------- | ----------- |
| id            |         **int**          |
| DivId         |         **int**          |
| notDivId      |         **int**          |
| synchDateTime | **str repr of datetime** |

---



## Order Invoice API
> GET POST

**@sha_required**
+ /api/tbl-dk-order-invoices/?startDate=<datetime>&endDate=<datetime>&DivId=<id>&notDivId=<id>
+ /api/tbl-dk-order-invoices/<OInvRegNo>/
+ /api/tbl-dk-order-inv-lines/?DivId=<id>&notDivId=<id>
+ /api/tbl-dk-order-inv-types/

> GET

## Filtering order invoices and invoices by datetime

**@sha_required** of **Synchronizer**

+ /api/tbl-dk-order-invoices/?startDate=<datetime>&endDate=<datetime>
+ /api/tbl-dk-invoices/?startDate=<datetime>&endDate=<datetime>

returns **all orders** if **blank**

(Provide **startDate** and **endDate**)
> **example request**
```url
/api/tbl-dk-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
```
> POST

**@token required** of **Rp_acc** login
+ /api/checkout-sale-order-inv/

+ /api/gen-reg-no/
```python
# example JSON for gen-reg-no
{
	"RegNumTypeId": 3,
	"random_mode": 1
}

# this will create a special RegNum and save in Pred_reg_num
```

+ /api/validate-order-inv-payment/
```python
# example of request to change the Order status
{
  "OInvRegNo": "ARSFFK43013",
  "ReqStr":"language=ru&orderId=934d3b94-b95e-45ea-ad2b-a114db47a411&password=e235erHw4784fwf&userName=103122512345"
}

# url_request: https://mpi.gov.tm/payment/rest/getOrderStatus.do?language=ru&orderId=934d3b94-b95e-45ea-ad2b-a114db47a411&password=e235erHw4784fwf&userName=103122512345

# output of the url_request will be like:
{
	"expiration": "206004",
	"cardholderName": "John Doe",
	"depositAmount": 123,
	"currency": "934",
	"approvalCode": "7****9",
	"authCode": 2,
	"ErrorCode": "0",
	"ErrorMessage": "Успешно",
	"OrderStatus": 2,
	"OrderNumber": "011**0******1",
	"Pan": "99*******51",
	"Amount": 123,
	"Ip": "***.***.***.***",
	"SvfeResponse": "0"
}
# OrderStatus == 2 means "Payment success"
# URL, Key and Value should be set in Config and .env
```

> GET

## Get all orders of a logged Rp_acc
**@token_required** of **Rp_acc** login
+ /api/v-order-invoices/?startDate=<datetime>&endDate=<datetime>
+ /api/v-order-invoices/paginate/?page=&endDate=&invStatus=&per_page=&sort=&invoices_only=
+ /api/v-invoices/?startDate=<datetime>&endDate=<datetime>

example:
	/api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948


## Get all order lines of a specific OInvRegNo if it's owner is Rp_acc
> GET

**@token_required** of **Rp_acc** login

Returns only if the **Rp_acc** is the **owner** of invoice
+ /api/v-order-invoices/<str:OInvRegNo>/


---