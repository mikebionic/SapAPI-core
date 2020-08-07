
# API authentication
Provide **username** and **password** in Authentication headers
+ /api/login/users/
+ /api/login/rp-accs/

# API config information
> GET
+ /api/api-config/

# Company information
> GET
+ /api/company-info/

# Simple data queries and insertions
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-barcodes/
+ /api/tbl-dk-res-prices/
+ /api/tbl-dk-res-totals/
+ /api/tbl-dk-images/
+ /api/tbl-dk-rp-acc-trans-totals/
+ /api/tbl-dk-total-transactions/
+ /api/tbl-dk-warehouses/
+ /api/tbl-dk-work-periods/


# Order invoice api
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-order-invoices/
+ /api/tbl-dk-order-invoices/<OInvRegNo>/
+ /api/tbl-dk-order-inv-lines/
+ /api/tbl-dk-order-inv-types/

> GET 

## Filtering order invoices by datetime

**@sha_required** of **Synchronizer**

+ /api/tbl-dk-order-invoices/?startDate=&endDate=

returns **all orders** if **blank**

(Provide **startDate** and **endDate**)
> **example request**
```url
/api/tbl-dk-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948
```
> POST 

**@token_required** of **Rp_acc** login
+ /api/checkout-sale-order-inv/

> GET 

## Get all orders of a logged Rp_acc
**@token_required** of **Rp_acc** login
+ /api/v-order-invoices/
+ /api/v-order-invoices/?startDate=2020-07-13 13:12:32.141562&endDate=2020-07-25 13:53:50.141948

## Get all order lines of a specific OInvRegNo if it's owner is Rp_acc
> GET 

**@token_required** of **Rp_acc** login

Returns only if the **Rp_acc** is the **owner** of invoice
+ /api/v-order-invoices/<str:OInvRegNo>/


# Resource category api
> GET POST
+ /api/tbl-dk-categories/

> GET
+ /api/tbl-dk-categories/<int:ResCatId>/

> GET
+ /api/tbl-dk-categories/paginate/

# Resource api
> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-resources/

> GET

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-resources/<int:ResId>/

## client view resource

> GET
+ /api/v-resources/
+ /api/v-full-resources/
+ /api/v-resources/<int:ResId>/
+ /api/tbl-dk-categories/<int:ResCatId>/v-resources/
+ /api/v-resources/search/?tag=<BarcodeVal or ResName>

> GET

from latest to first (needs configurations for datetime order
+ /api/v-resources/paginate/
+ /api/v-resources/paginate/?offset=<lastId>&limit=<quantity>

> GET POST

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-rp-accs/
+ /api/tbl-dk-users/

> GET

**@sha_required** of **Synchronizer**
+ /api/tbl-dk-rp-accs/<int:RpAccRegNo>/
+ /api/tbl-dk-users/<int:UId>/
+ /api/tbl-dk-sliders/