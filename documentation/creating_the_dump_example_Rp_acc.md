creating the dump example Rp_acc in activation for reso activation;

```sql
insert into tbl_dk_rp_acc ("RpAccName", "DbGuid", "DeviceQty", "RpAccGuid", "RpAccRegNo", "RpAccTypeId", "RpAccStatusId") values ('SapMobileResoAgent', 'aafbf1a1-d0b5-45d4-9868-3e470e7704e1', 5, 'bbcbf1a1-d0b5-45d4-9868-3e470e7704e2', 'SAPRESTO', 2, 1);
```

checking query
```sql
select ("DevId", "DevUniqueId", "UId", "RpAccId", "IsAllowed") from tbl_dk_device ;
```