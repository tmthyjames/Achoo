# Achoo Environment Setup

### Dependencies:

You will need the following installed on your OS of choice to run Achoo:
 * Python 3
 * R
 * PostgreSQL
 * PostGIS with command line tools

We recommend using a [virtualenv](https://docs.python.org/3/library/venv.html) to manage Python dependencies.

To install the Python dependencies, run the following from the project root:

`pip install -r requirements.txt`


# Flask
### Environment Variables:

Variable Name | Value
--- | ---
`ACHOO_SECRET_KEY` | [Key for signing things](http://flask.pocoo.org/docs/0.12/api/#flask.Flask.secret_key), set to strong random value.
`ACHOO_PG_CONN_STR` | [SQLAlchemy database URI (PostgreSQL)](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls). Something like `postgresql://user@localhost:5432/achoo`.
`ACHOO_GOOGLE_MAPS_API_KEY` | [Google Maps API Key](https://developers.google.com/maps/documentation/javascript/get-api-key).

### Bootstrap the Database for the first time

From the application root directory, run the following in a python interpreter to create the database and tables:

```python
from app.models.models import db
db.create_all()
```

Initialize PostGIS:

```bash
psql achoo
CREATE EXTENSION postgis;
\q
```

Download and import GIS shapefiles and clean up:

```bash
mkdir gisdata
cd gisdata
wget http://www2.census.gov/geo/tiger/GENZ2016/shp/cb_2016_us_zcta510_500k.zip
unzip cb_2016_us_zcta510_500k.zip
shp2pgsql cb_2016_us_zcta510_500k.shp > gisdata.sql
psql achoo < gisdata.sql
cd ..
rm -r gisdata
```

### Run the Web Application

```bash
python3 application.py
```

Or:

```bash
export FLASK_PATH=/path/to/Achoo/application.py
flask run --reload
```


# Analytics
TODO