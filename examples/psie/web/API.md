## API

### Search API

#### endpoint
- GET /api/search

#### parameters
- q: query string
- p: page (first page = 1)
- geo: location filter. (geo json format)
- from: issue_date filter (date format: YYYY-MM-DD)
- to: issue_date filter (date format: YYYY-MM-DD)

#### sample request
```sh
curl http://54.199.246.169:8082/api/search?q=japan
```

#### response
```json
{
  "docs": [
    {
      "publisher": "NOAA National Oceanographic Data Center (Resource Provider)",
      "title": "The results of the oceanographic observations in the Sea of Japan from 04 February 1971 to 27 February 1971 (NODC Accession 7101191)",
      "issue_date": "2003-10-23T22:00:00Z",
      "spatial_bounds": "{\"type\": \"Polygon\", \"coordinates\": [[[131.0, 35.0], [140.0, 35.0], [140.0, 42.0], [131.0, 42.0], [131.0, 35.0]]]}",
      "id": 9532
    },
    ...
  ],
  "hits": 103
}
```

### Detail API

#### endpoint
- GET /api/detail/ID

#### parameters
none

#### sample request

```sh
curl http://54.199.246.169:8082/api/detail/9532
```

#### response
```json
{
  "publication": {
    "last_update_date": "2013-06-02T21:00:00",
    "updated_at": "2014-05-07T18:24:56.091159",
    "catalog_id": 5,
    "access_level": "public",
    "upload_date": null,
    "bureau_code": "006:48",
    "keywords": "",
    "license": null,
    "spatial_bounds": "{\"type\": \"Polygon\", \"coordinates\": [[[131.0, 35.0], [140.0, 35.0], [140.0, 42.0], [131.0, 42.0], [131.0, 35.0]]]}",
    "temporal_bounds": "1971-02-04/1971-02-27",
    "contact_email": "NODC.DataOfficer@noaa.gov",
    "issue_date": "2003-10-23T22:00:00",
    "access_level_comment": null,
    "id": 9532,
    "publisher": "NOAA National Oceanographic Data Center (Resource Provider)",
    "title": "The results of the oceanographic observations in the Sea of Japan from 04 February 1971 to 27 February 1971 (NODC Accession 7101191)",
    "crawl_time": "2014-05-01T06:46:17",
    "update_frequency": "asNeeded",
    "release_date": null,
    "description": "",
    "language": null,
    "catalog_record_id": "6886f516-bebf-43f2-bab4-24b05aba0849",
    "category": "",
    "contact_phone": null,
    "created_at": "2014-05-07T18:24:56.091159",
    "data_quality": null,
    "program_code": null,
    "url": "http://www.doc.gov/data.json",
    "contact_name": null
  },
  "components": [
    {
      "filename": "8600245",
      "content_type": "text/html; charset=UTF-8",
      "file_type": "text/html",
      "subcomponents": [],
      "status_code": 200,
      "size": 7997,
      "id": 12799,
      "crawl_time": "2014-05-19T16:53:41",
      "label": "accessURL"
     },
     ...
  ]
}
```
