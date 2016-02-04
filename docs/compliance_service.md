# Compliance Service

## Uploading content

A client should POST to /upload with either the file data or the OPeNDAP URL.
The response will be a `job_id`. The `job_id` is used to view the report and
view the job's processing status.

### For OPeNDAP Requests

POST /upload

Accepts two form fields:

 - `checker`
 - `url`

`checker` must be one of the following:
 - `cf`
 - `gliderdac`
 - `acdd`

These correspond to the command line test names.

`url` should be a valid OPeNDAP URL endpoint.

### Example

```
curl --data "checker=cf&url=http%3A%2F%2Fgeoport-dev.whoi.edu%2Fthredds%2FdodsC%2Fusgs%2Fdata2%2Femontgomery%2Fstellwagen%2FCF-1.6%2FCAPE_COD_BAY%2F3051B-A.cdf" -XPOST http://data.ioos.us/compliance/upload
```

## Response

```json
{
  "job_id": "96e5861b787677d7c6da8971a4b7472c45825bfd",
  "message": "Check successful"
}
```


## Checking the Job and viewing the results

```
GET /api/job/<job_id>
```

This endpoint will return an HTTP 404 if the job is either expired or not yet
done processing. Jobs will expire after one hour.

If there is an error in processing the endpoint will return a 400 and indicate
what the problem is.

### On Error

```json
{
  "error":"IOError",
  "message":"Unable to connect to remote endpoint"
}
```

### Resposne

```json
{
  "all_priorities": [
    {
      "children": [],
      "msgs": [],
      "name": "2.2 valid netcdf data types",
      "value": [
        23,
        23
      ],
      "weight": 3
    },
    {
      "children": [],
      "msgs": [],
      "name": "2.3 legal variable names",
      "value": [
        23,
        23
      ],
      "weight": 3
    }
  ],
  "high_count": 1,
  "high_priorities": [

  ],
  "low_count": 0,
  "low_priorities": [
  ],
  "medium_count": 0,
  "medium_priorities": [
  ],
  "possible_points": 343,
  "scored_points": 342,
  "source_name": "http://geoport-dev.whoi.edu/thredds/dodsC/usgs/data2/emontgomery/stellwagen/CF-1.6/CAPE_COD_BAY/3051B-A.cdf",
  "testname": "cf"
}
```

The `_count` keys indicate how many total items which didn't receive a perfect
score. The `all_priorities` key contains all of the checks that were performed.
The other three `_priorities` keys contain the appropriate checks for that
level.


