# Installation

I recommend using a virtual environment to install the dependencies, I am
using virtualenv in these instructions.

```bash
git clone https://github.com/nwinston/fetch.git
```
Navigate to root of the repository and run:

```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Running
```bash
export FLASK_APP=fetch/app.py
flask run
```

This will start the web server on port 5000.

# Calling the API

The web server exposes the following endpoints:

## POST /api/\<user\>/create
This endpoint will create a new user.

```bash
curl -XPOST 'localhost:5000/api/user1/create'
```
Will return

```json
{"response":{},"success":true}
```



## POST /api/\<user\>/transaction

  This endpoint will create a new transaction.

  ```bash
    curl -L -X POST 'localhost:5000/api/user1/transaction' -H 'Content-Type: application/json' \
    --data-raw {"timestamp":"2020-10-31T11:00:00Z", "payer":"UNILEVER", "points":"20000"} 
   ```

Will return
```json
{"response":{},"success":true}
```

## POST /api/\<user\>/spend
This endpoint will spend points for a user.
```bash
curl -L -X PUT localhost:5000/api/user1/spend -H 'Content-Type: application/json' --data-raw '{"points": "5000"}'
```

Will return
```json
{
    "response": {
        "DANNON": -100,
        "UNILEVER": -4900
    },
    "success": true
}
```

## GET /api/\<user\>/points

This endpoint will return the points for a user. It accepts a query parameter itemized.
If itemized is true, it will return the balances for each payer. If false, it will return the total points.

```bash
curl -L -X GET 'localhost:5000/api/user1/points?itemized=true'
```

Will return

```json
{
    "response": {
        "DANNON": 0,
        "UNILEVER": 15300
    },
    "success": true
}
```
