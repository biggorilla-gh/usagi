## API Server

### boot

```sh
python api_server.py
```

## API

### endpoint

GET /api/search

### parameters

- q : query

### sample request

```sh
curl http://54.199.246.169:8085/api/search?q=emp
```

### response
```json
{
  "docs":[
    {"title": "Employees"},
    {"title": "Customers"}
  ],
  "hits": 2
}
```
