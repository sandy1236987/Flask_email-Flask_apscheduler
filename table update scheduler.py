from flask import Flask
import pymysql
from flask_mail import Mail,Message
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app 
import time
from threading import Thread
import smtplib

app = Flask(__name__)

def db_init():
    with app.app_context():
      db = pymysql.connect(
        host = 'ec2-34-208-156-155.us-west-2.compute.amazonaws.com',
        user = 'erp',
        password = 'erp',
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

def UPDATE():
    # with app.app_context():
    db,cursor=db_init()
    cursor.execute('UPDATE `me_boss`,`sales` SET `me_boss`.`PO_Number`=`sales`.`PO_Number`, `me_boss`.`PO_Name`=`sales`.`PO_Name`, `me_boss`.`Team`=`sales`.`Team`, `me_boss`.`Reseller`=`sales`.`Reseller`, `me_boss`.`End_Customer`=`sales`.`End_Customer`, `me_boss`.`type`=`sales`.`type`, `me_boss`.`Status`=`sales`.`Status`, `me_boss`.`delete_by_sales`=`sales`.`delete_by_sales`, `me_boss`.`Renewal_Date`=`sales`.`Renewal_Date`, `me_boss`.`Auto_Renewal_Term`=`sales`.`Auto_Renewal_Term`, `me_boss`.`Profit(USD)`=`sales`.`Profit(USD)`, `me_boss`.`cost(USD)`=`sales`.`cost(USD)`, `me_boss`.`take_a_cut(%)`=`sales`.`take_a_cut(%)`, `me_boss`.`Price(USD)`=`sales`.`Price(USD)` WHERE `me_boss`.`Purchase _Order_Number`=`sales`.`Purchase_Order_Number`;')
    db.commit()
    cursor.close()
    db.close()    
    print('job_cron1 executed') 


if __name__ == "__main__":
    scheduler.add_job(func=UPDATE,id='job_cron1', trigger='cron', day='*', hour=10 ,minute=48)
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
    # while True:
    #     print(time.time())
    #     time.sleep(5)
    