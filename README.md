# appsync-tools

Parses aurora and dynamodb responses into a more usable format.

Aurora results are returned as a list of dictionaries with the column names being the key.
Nulls (returned by Aurora as isNull) are returned as None types. Any value that can be parsed as json is cast from a string to a list/dictionary.
Responses are returned formated as:

```json

  [
    {"columnOneName": "value", "columnTwoName": "value"},
    {"columnOneName": "value", "columnTwoName": "value"}
  ]
```

Where each item in the top level array is a separate row.

Dynamodb results are returned as either a dictionary (for get_item operations) or a list of dictionaries (query).


Pretty parsing Aurora records
-----------------------------

pretty_parse_aurora(records, type_attribute=None) -> list

**Arguments:**
- records -- The records from the API query (execute_statement()["records"])

**Keyword Args:**
- type_attribute -- If used will pass results to typify(results, type_attribute=type_attribute) before returning


```python

  from appsync_tools import pretty_parse_aurora

  response = client.execute_statement(
      secretArn=environ["PG_SECRET"],
      database=environ["DB_NAME"],
      parameters=parameters,
      resourceArn=environ["DB_ARN"],
      includeResultMetadata=True,
      sql=sql
  )
  print(pretty_parse_aurora(response))
```


Parsing Dynamodb records
----------------------------

pretty_parse_dynamo(records, type_attribute=None) -> list | dict

**Arguments:**
- records -- The Item(s) from a call to query, get_item

**Keyword Args:**
- type_attribute -- If used will pass results to typify(results, type_attribute=type_attribute) before returning

```python

  from appsync_tools import pretty_parse_dynamo

  response = client.get_item(
    Key={"pk": "foo", "sk": "bar"}
  )
  print(response.get("Item"))
```


Adding __typename to all records based on an attribute
------------------------------------------------------

typify(records, type_attribute="type") -> list | dict
**Arguments:**
records -- The Item(s) from a call to query, get_item
**Keyword Args:**
type_attribute -- Attribute name that contains the __typename value

Example
----------------------------

```python

  from appsync_tools import typify

  response = client.get_item(
    Key={"pk": "foo", "sk": "BarType"}
  )

  print(typify(response.get("Item"), type_attribute="sk"))
```
