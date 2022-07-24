from flask import Flask
import pymysql
from flask_mail import Mail,Message
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app 
import time
from threading import Thread
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)


app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = '',
    MAIL_PASSWORD=  '',
    MAIL_DEFAULT_SENDER= ''
)
mail = Mail(app)
email_sender=''
email_password=''
def db_init():
    with app.app_context():
      db = pymysql.connect(
        host = '',
        user = '',
        password = '',
        database='metaage_sales',
        port = 3306
    )
      cursor = db.cursor(pymysql.cursors.DictCursor)
      return db, cursor

class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Taipei'
app.config.from_object(Config())
scheduler = APScheduler(BackgroundScheduler(timezone='Asia/Taipei'))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
 
def send_mail():
    with app.app_context():
      db,cursor=db_init()
      cursor.execute('SELECT `me_boss`.`PO_Number`,`me_IT`.`Email`,TIMESTAMPDIFF(DAY, now(),`Renewal_Date`) AS daytype FROM `metaage_sales`.`me_boss`,`me_IT`HAVING daytype<=30 AND daytype>0;')
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        detail = cursor.fetchall()
        db.commit()
        for i in detail:
           msg = Message(subject='ERP',body='Hello ' + str(i['PO_Number'])+ 'Thanks For using our services.',recipients=[str(i['Email'])])
           Thread(target=mail.send(msg)).start() 
      cursor.close()
      db.close()    
      print('job_cron1 executed') 

if __name__ == "__main__":
    scheduler.add_job(func=send_mail,id='job_cron1', trigger='cron', day='*', hour=11 ,minute=3)
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
    
