
# API authentication
/api/login/users/
/api/login/rp-accs/

# Simple data queries and insertions
GET POST
/api/tbl-dk-barcodes/

GET POST
/api/tbl-dk-res-prices/

GET POST
/api/tbl-dk-res-totals/

GET POST
/api/tbl-dk-images/

GET POST
/api/tbl-dk-rp-acc-trans-totals/
/api/tbl-dk-total-transactions/

GET POST
/api/tbl-dk-order-invoices/

GET POST
/api/tbl-dk-order-inv-lines/

GET POST
/api/tbl-dk-order-inv-types/

GET POST
/api/tbl-dk-warehouses/

GET POST
/api/tbl-dk-categories/

GET PUT
/api/tbl-dk-categories/<int:ResCatId>/

GET
/api/tbl-dk-categories/paginate/

GET POST
/api/tbl-dk-resources/

GET PUT
# short db info
/api/tbl-dk-resources/<int:ResId>/

GET
/api/v-resources/
/api/v-full-resources/

GET
# wide api info
/api/v-resources/<int:ResId>/

GET
/api/tbl-dk-categories/<int:ResCatId>/v-resources/

GET
# from latest to first (needs configurations for datetime order)
# withoud any initial data
/api/paginate/v-resources/
/api/paginate/v-resources/?last=<lastId>&limit=<quantity>


GET POST
/api/tbl-dk-rp-accs/

GET
/api/tbl-dk-rp-accs/<int:RpAccId>/

GET POST
/api/tbl-dk-users/

GET
/api/tbl-dk-users/<int:UId>/

GET
/api/tbl-dk-sliders/

POST [Token required of Rp_acc login]
/api/checkout-sale-order-inv/