# csinvest-connector

## Generate a Model with curl

```bash
curl -s --request POST \
  --url https://cs.deals/API/IPricing/GetSalesHistoryMulti/v1 \
  --header 'Content-Type: application/json' \
  --data '{"items":[{"name":"Revolution Case","appid":730}]}' \
| datamodel-codegen \
    --output src/connector/csdeals/models/get_sales_history_multi.py \
    --output-model-type pydantic_v2.BaseModel \
    --force-optional \
    --class-name GetSalesHistory
```
