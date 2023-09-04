# Rows api

A basic api to generate a list of row numbers

## Usage

- request parameter: `rows_amount` (integer)

Example request:

```json
{
    "rows_amount": 10
}
```

Response:

```json
{
    "rows": [
        {
            "row": 1
        },
        {
            "row": 2
        },
        {
            "row": 3
        },
        {
            "row": 4
        },
        {
            "row": 5
        },
        {
            "row": 6
        },
        {
            "row": 7
        },
        {
            "row": 8
        },
        {
            "row": 9
        },
        {
            "row": 10
        }
    ]
}
```

## Security

The api is protected by a `x-api-key` header parameter. The key can be set as docker environment variable `KEY`