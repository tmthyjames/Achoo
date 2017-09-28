# utils.py

import datetime
import smtplib
import time

from bs4 import BeautifulSoup as BS
import requests
import sqlalchemy

import constants as const


def send_email(subject, text):
    """Send email using Gmail"""
    message = "\From: {}\nTo: {}\nSubject: {}\n\n{}".format(
        const.GMAIL_FROM, ",".join(const.GMAIL_TO), subject, text)
    try:
        server = smtplib.SMTP(const.SMTP_URI, const.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(const.GMAIL_FROM, const.GMAIL_PASSWORD)
        server.sendmail(const.GMAIL_FROM, const.GMAIL_TO, message)
        server.close()
    except Exception as e:
        print(e)


def get_db_engine():
    """Get database engine"""
    return sqlalchemy.create_engine(const.POSTGRES_URI)


def get_uri_content(uri, headers=None, content_type='json'):
    """Get URI content"""
    assert content_type in set(['json', 'html', 'text']), 'bad type {}'.format(content_type)
    resp = requests.get(uri, headers=headers)
    if content_type == 'json':
        return resp.json()
    elif content_type == 'html':
        return BS(resp.content, 'html')
    return resp.content


def get_current_time(no_wrap=False):
    """Get current time"""
    cur_time = datetime.datetime.now().timetuple()
    if no_wrap is True:
        return cur_time
    return time.mktime(cur_time)
