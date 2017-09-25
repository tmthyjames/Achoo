import os
import sqlalchemy

FROM = os.environ['FROM_EMAIL']
TO = os.environ['TO_EMAIL']
GMAIL_PASSWORD = os.environ['GMAIL_PASSWORD']

def send_email(TO, FROM, subject, text):
    import smtplib
    gmail_user = FROM
    gmail_pwd = GMAIL_PASSWORD
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), subject, text)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) 
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except Exception as e:
        print e

engine = sqlalchemy.create_engine('postgresql://'+os.environ['USERNAME']+':'+os.environ['PASSWORD']+'@'+os.environ['HOSTNAME']+':5432/allergyalert')
results = engine.execute('select * from results order by dateof desc limit 1').fetchone()
prediction = results.prediction

if prediction >= .6:
    send_email([FROM], TO, 'Take Action', 'Preemptive action may be necessary')