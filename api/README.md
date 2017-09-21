## API Server

### boot

```sh
python server.py
```

## API

### endpoint

GET /api/search

### parameters

- q : query (optional, default: "")
- path : path (optional, default: "")

### sample request

```sh
curl http://54.199.246.169:8085/api/search?q=emp
curl http://54.199.246.169:8085/api/search?q=emp&path=ClassicModels
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

### endpoint

GET /api/filters

### parameters

- depth : filter depth (optional, default: 1)

### sample request

```sh
curl http://54.199.246.169:8085/api/filters?depth=2
```

### response
```json
[
  {
	"id": 5,
    "parent_id": 0,
	"name": "employees sakila sportsdb",
	"children": [
	  {"parent_id": 5, "id": 6, "name": "sakila"},
	  {"parent_id": 5, "id": 7, "name": "sportsdb"},
	  {"parent_id": 5, "id": 8, "name": "employees"}
	]
  }
]
```
