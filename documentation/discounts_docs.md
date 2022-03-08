
Discount types:

| DiscTypeId | DiscTypeName_enUS | DiscTypeDesc_enUS             |
| ---------- | ----------------- | ----------------------------- |
| 1          | Discount %        | Persentage discount           |
| 2          | Discount points   | Discount in cumulative points |
| 3          | Gift (Free)       | To sell as free               |
| 4          | Purchace price    | To sell by purchace price     |

Res_discount db structure

| Column              | Type                        | Collation | Nullable | Default           |
| ------------------- | --------------------------- | --------- | -------- | ----------------- |
| ResDiscId           | integer                     |           | not null | nextval           |
| SaleCardId          | integer                     |           |          |
| ResDiscRegNo        | character varying(100)      |           | not null |
| SaleResId           | integer                     |           |          |
| SaleResAmount       | real                        |           |          | 0                 |
| DiscTypeId          | integer                     |           |          |
| DiscValue           | real                        |           | not null | 0.0               |
| DiscDesc            | character varying(500)      |           |          | ''::              |
| ResDiscStartDate    | timestamp without time zone |           |          |
| ResDiscEndDate      | timestamp without time zone |           |          |
| ResDiscIsActive     | boolean                     |           | not null | true              |
| GiftResId           | integer                     |           |          |
| GiftResAmount       | real                        |           |          | 0                 |
| GiftResDiscValue    | real                        |           |          | 0                 |
| AddInf1             | character varying(500)      |           |          | ''::              |
| AddInf2             | character varying(500)      |           |          | ''::              |
| AddInf3             | character varying(500)      |           |          | ''::              |
| AddInf4             | character varying(500)      |           |          | ''::              |
| AddInf5             | character varying(500)      |           |          | ''::              |
| AddInf6             | character varying(500)      |           |          | ''::              |
| CreatedDate         | timestamp without time zone |           |          | CURRENT_TIMESTAMP |
| ModifiedDate        | timestamp without time zone |           |          | CURRENT_TIMESTAMP |
| CreatedUId          | integer                     |           |          | 0                 |
| ModifiedUId         | integer                     |           |          | 0                 |
| SyncDateTime        | timestamp without time zone |           |          |
| OptimisticLockField | integer                     |           |          |
| GCRecord            | integer                     |           |          |
| ResDiscGuid         | uuid                        |           |          |

> Insert discount:

```sql
insert into tbl_dk_res_discount ("ResDiscRegNo", "SaleResId", "DiscValue", "SaleResAmount", "DiscTypeId", "ResDiscIsActive") values ('TestDisc1', 4, 80, 1, 1, true);
```