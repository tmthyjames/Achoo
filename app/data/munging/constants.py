# constants.py

import os


# Postgres config
POSTGRES_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.environ['ACHOO_DB_USERNAME'],
    os.environ['ACHOO_DB_PASSWORD'],
    os.getenv('ACHOO_DB_HOSTNAME', 'localhost'),
    os.getenv('ACHOO_DB_PORT', '5432'),
    os.getenv('ACHOO_DB_DATABASE', 'achoo')
)

# Airnow config
AIRNOW_URI = 'https://www.airnow.gov/index.cfm?action=airnow.local_city&zipcode=37076&submit=Go'

# Pollen config
POLLEN_URI = 'https://www.pollen.com/api/forecast/current/pollen/' + os.environ['ACHOO_POLLEN_ZIPCODE']
POLLEN_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8,it;q=0.6',
    'connection': 'keep-alive',
    'cookie': 'ASP.NET_SessionId=udv21cgxl23lrxupoxt5eowg; geo=37076; __RequestVerificationToken=WNDbD03-8Abz7c7XERainKA6bQpRKizwCgCNLLpzxW5ALMV7MMTTOob2wTbI9q2UIwuDJOR68xz084_DBlRKN3EYfJ1vedX2M63WyCZXnzM1; _gat=1; _ga=GA1.2.1454068007.1505789851; _gid=GA1.2.1546508119.1505789851; session_depth=www.pollen.com%3D3%7C668625674%3D3',
    'host': 'www.pollen.com',
    'referer': 'https://www.pollen.com/forecast/current/pollen/37076',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'cache-control': 'no-cache'
}

# Gmail config
GMAIL_FROM = os.environ['ACHOO_FROM_EMAIL']
GMAIL_TO = os.environ['ACHOO_TO_EMAIL']
GMAIL_PASSWORD = os.environ['ACHOO_GMAIL_PASSWORD']
SMTP_URI = 'smtp.gmail.com'
SMTP_PORT = 587

# Dark Sky config
DARK_SKY_URI = 'https://api.darksky.net/forecast/{}/{}'.format(
    os.environ['ACHOO_DARK_SKY_API_KEY'],
    os.environ['ACHOO_DARK_SKY_LOCATION']
)
