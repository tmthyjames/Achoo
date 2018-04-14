# Achoo Development Environment Setup

### Dependencies:

You need Python 3 and PostgreSQL installed to run Achoo.

To install Python dependencies, run the following from the project root:

`pip install -r requirements.txt`

We recommend using a [virtualenv](https://docs.python.org/3/library/venv.html) to manage Python dependencies.

### Environment Variables:

Variable Name | Value
--- | ---
`ACHOO_SECRET_KEY` | [Key for signing things](http://flask.pocoo.org/docs/0.12/api/#flask.Flask.secret_key), set to strong random value.
`ACHOO_PG_CONN_STR` | [SQLAlchemy database URI (PostgreSQL)](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls). Something like `postgresql://user@localhost:5432/achoo`.
`ACHOO_GOOGLE_MAPS_API_KEY` | [Google Maps API Key](https://developers.google.com/maps/documentation/javascript/get-api-key).

### Bootstrap the Database for the first time

From the application root directory, run the following in a python interpreter to create the database and tables:

```
from app.models.models import db
db.create_all()
```
