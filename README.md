This is a port of [gocmdpev](https://github.com/simon-engledew/gocmdpev) 

# Usage:
  prefix your query with `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)`

this will return you a json string that can be passed to the visualizer
visualiser takes 2 params:
terminal_width = default 100
color_mode_on = default True

```
from pyev import Visualizer
for explain in parsed_json:
    v = Visualizer(160, True)
    v.load(explain)
    v.print()
```
to read json from a file use
```
from pyev import Visualizer
import json

def visualize():
    with open("query_plan_full.json") as json_file:
        explains = json.load(json_file)
        for explain in explains:
            v = Visualizer()
            v.load(explain)
            v.print()
visualize()
```

example output:
```
○ Total Cost: 808.5400000000001
○ Planning Time: 25.86 ms
○ Execution Time: 1.86 s
┬
│
└─⌠ Unique 
  │ Not found : Unique
  │ ○ Duration: <1 ms (0%)
  │ ○ Cost: 0 (0%)
  │ ○ Rows: 1
  ├►  customers.number
  │
  └─⌠ Sort 
    │ Sorts a record set based on the specified sort key.
    │ ○ Duration: <1 ms (0%)
    │ ○ Cost: 0 (0%)
    │ ○ Rows: 1
    ├►  customers.number
    │
    └─⌠ Nested Loop 
      │ Merges two record sets by looping through every record in the first set
      │ and trying to find a match in the second set. All matching records are
      │ returned.
      │ ○ Duration: 730.10 ms (20%)
      │ ○ Cost: 0 (0%)
      │ ○ Rows: 1
      │   Inner join
      ├►  customers.number
      │
      └─⌠ Nested Loop bad estimate
        │ Merges two record sets by looping through every record in the first
        │ set and trying to find a match in the second set. All matching records
        │ are returned.
        │ ○ Duration: 0.69 s (37%)
        │ ○ Cost: 48 (6%)
        │ ○ Rows: 785
        │   Inner join
        │   rows Underestimated by 785.00x
        ├►  customers.number + customers.id + customers.blocked
        │  + customers.accepts_notifications + m3.id
        │
        └─⌠ Nested Loop bad estimate
          │ Merges two record sets by looping through every record in the first
          │ set and trying to find a match in the second set. All matching
          │ records are returned.
          │ ○ Duration: 3.74 ms (0%)
          │ ○ Cost: 7 (1%)
          │ ○ Rows: 760
          │   Inner join
          │   rows Underestimated by 108.57x
          ├►  m2.recipient_phone + (unnest('{12345000000}'::text[]) + m3.id
          │
          └─⌠ Nested Loop 
            │ Merges two record sets by looping through every record in the
            │ first set and trying to find a match in the second set. All
            │ matching records are returned.
            │ ○ Duration: 0.80 s (43%)
            │ ○ Cost: 808 (100%)
            │ ○ Rows: 760
            │   Inner join
            │   rows Underestimated by 19.00x
            ├►  m2.recipient_phone + m2.marketing_campaign_settings_id +
            │  (unnest('{12345000000}'::text[]))
            │
            └─⌠ Aggregate [Hashed] largest
              │ Groups records together based on a GROUP BY or aggregate
              │ function (e.g. sum()).
              │ ○ Duration: 1.11 ms (0%)
              │ ○ Cost: 4 (1%)
              │ ○ Rows: 1,000
              │   rows Overestimated by 0.20x
              ├►  (unnest('{12345000000}'::text[]))
              │
              └─⌠ ProjectSet largest
                │ Not found : ProjectSet
                │ ○ Duration: <1 ms (0%)
                │ ○ Cost: 1 (0%)
                │ ○ Rows: 1,000
                ├►  unnest('{12345000000}'::text[])
                │
                └─⌠ Result 
                  │ Not found : Result
                  │ ○ Duration: <1 ms (0%)
                  │ ○ Cost: 0 (0%)
                  │ ○ Rows: 1
            │
            └─⌠ Index Scan [Forward] slowest
              │ Finds relevant records based on an Index. Index Scans perform 2
              │ read operations: one to read the index and another to read the
              │ actual value from the table.
              │ ○ Duration: 0.80 s (43%)
              │ ○ Cost: 4 (1%)
              │ ○ Rows: 1
              │   on public.marketing_offers
              │   using index_offers_on_recipient_phone_and_provider_id
              │   filter (m2.created_at > '2021-07-05 14:00:00'::timestamp without time zone) [-1 rows]
              ⌡► m2.recipient_phone + m2.marketing_campaign_settings_id
          │
          ├─⌠ Index Scan [Forward] 
          │ │ Finds relevant records based on an Index. Index Scans perform 2
          │ │ read operations: one to read the index and another to read the
          │ │ actual value from the table.
          │ │ ○ Duration: 3.04 ms (0%)
          │ │ ○ Cost: 0 (0%)
          │ │ ○ Rows: 1
          │ │   on public.marketing_campaign_settings
          │ │   using marketing_campaign_settings_pkey
          │ │   filter (m3.campaign_category = 4) [-0 rows]
          │ ⌡► m3.id + m3.provider_id + m3.marketing_campaign_id +
          │    m3.campaign_category + m3.current + m3.value + m3.discount_type +
          │    m3."limit" + m3.valid_for + m3.created_at + m3.updated_at +
          │    m3.all_services + m3.automatic_discount_id
        │
        └─⌠ Index Scan [Forward] 
          │ Finds relevant records based on an Index. Index Scans perform 2 read
          │ operations: one to read the index and another to read the actual
          │ value from the table.
          │ ○ Duration: 0.69 s (37%)
          │ ○ Cost: 8 (1%)
          │ ○ Rows: 1
          │   on public.customers
          │   using index_customers_on_number
          │   filter ((customers.deleted_at IS NULL) AND (customers.provider_id = 129155)) [-2 rows]
          ⌡► customers.number + customers.id +
             customers.blocked + customers.accepts_notifications
      │
      ├─⌠ Index Scan [Forward] costliest
      │ │ Finds relevant records based on an Index. Index Scans perform 2 read
      │ │ operations: one to read the index and another to read the actual value
      │ │ from the table.
      │ │ ○ Duration: 730.05 ms (20%)
      │ │ ○ Cost: 2 (0%)
      │ │ ○ Rows: 0
      │ │   on public.customer_payments_accumulators
      │ │   using index_customer_payments_id
      │ │   filter (c1.unpaid_amount > '0'::numeric) [-1 rows]
      │ ⌡► c1.id + c1.customer_id + c1.provider_id + c1.unpaid_amount +
      │    c1.created_at + c1.updated_at
```
