# Welcome to Sap Api documentation!
This documentation provides an info about routes and their usage, use it for building client-side applications.


## Legend
Shortcut                    | Description
----------------------------|------------ 
**!!**                      | Warning sign
**!! Out of support**       | Route might be updated to different route and will be deleted after a major update process and verification
**@sha required**           | Requires api key of **Synchronizer** for **@sha required**
**@token required**   			| **@token required** of **Rp acc** login
---


## Authentication API
Provide **username** and **password** in Authentication headers

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|---------
/api/login/                    | **GET**             | Updated    |

**Properties**
__Name__             | __Type__    | __Description__ | __Example__
---------------------|-------------|-----------------|------------
user                 | **str**     | validates the User model
rp_acc               | **int**     | validates the Rp_acc model

---

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/login/users/              | **GET**             | Active     | **!! Out of support**
/api/login/rp-accs/            | **GET**             | Active     | **!! Out of support**

---


## Fetch information API

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/api-config/               | **GET**             | Active     | API config information
/api/company-info/             | **GET**             | Active     | Company and Division information
/api/api-config/               | **GET**             | Active     | API config information


---


## Synchronizing, data queries and insertions API

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/company/                  | **GET** **POST**    | Active     | **@sha required**

**Properties**
__Name__             | __Type__    | __Description__ | __Example__
---------------------|-------------|-----------------|------------
CGuid                | **str**     |

---

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/division/                  | **GET** **POST**    | Active     | **@sha required**

**Properties**
__Name__             | __Type__    | __Description__ | __Example__
---------------------|-------------|-----------------|------------
DivGuid              | **str**     |

---

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/tbl-dk-barcodes/          | **GET** **POST**    | Updated    | **@sha required**

**Properties**
__Name__             | __Type__         | __Description__ | __Example__
---------------------|------------------|-----------------|------------
id                   | **int**          |
val                  | **str**          |
synchDateTime        | **datetime**     |
DivId                | **int**          |
notDivId             | **int**          |


---

__Route__                      | __Methods__         | __Status__ | __Note__
-------------------------------|---------------------|------------|--------
/api/tbl-dk-res-prices/         | **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-res-totals/         | **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-images/             | **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-rp-acc-trans-totals/| **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-total-transactions/ | **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-warehouses/         | **GET** **POST**    | Active     | **@sha required**
/api/tbl-dk-work-periods/       | **GET** **POST**    | Active     | **@sha required**


**Properties**
__Name__             | __Type__         | __Description__ | __Example__
---------------------|------------------|-----------------|------------
synchDateTime        | **datetime**     |
DivId                | **int**          |
notDivId             | **int**          |

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

# this will create a special RegNum and save in Pred_regnum
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

## Payment info from database
+ /api/tbl-dk-payment-methods/
+ /api/tbl-dk-payment-types/

## Brands
+ /api/tbl-dk-brands/?id=<brandId>&name=<brandName>

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


## Resource category api
> GET POST

+ /api/tbl-dk-categories/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>

> GET

+ /api/tbl-dk-categories/<int:ResCatId>/

> GET

+ /api/tbl-dk-categories/paginate/

## Resource api
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-resources/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>&id=<id>&regNo=<regNo>&name=

## client view resource

> GET

+ /api/v-resources/?DivId=<id>&notDivId=<id>
+ /api/v-full-resources/?DivId=<id>&notDivId=<id>
+ /api/v-resources/<int:ResId>/

**!! Warning** old version routes, supported til major update and verification
Use **/resources/** route with argument property **category**
+ /api/tbl-dk-categories/<int:ResCatId>/v-resources/?DivId=<id>&notDivId=<id>

	**Pagination and search**
+ /api/resources/?sort=<sort>&category=<categoryId>&brand=<brandId>&per_page=<per_page>&page=<page>&search=<search>&DivId=<divId>&notDivId=<notDivId>

> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-rp-accs/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>&id=<id>&regNo=<regNo>&name=
+ /api/tbl-dk-users/?synchDateTime=<datetime>&DivId=<id>&notDivId=<id>&id=<id>&regNo=<regNo>&name=

> GET

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-sliders/?DivId=<id>&notDivId=<id>&name=<name>&id=<id>

**!! Warning** old version routes, supported til major update and verification
+ /api/tbl-dk-sliders/<SlName>/