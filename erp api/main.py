from flask import Flask
from flask_restful import Resource
import pymysql
from flask_apispec import use_kwargs
from flask import request
from marshmallow import fields
from werkzeug.security import generate_password_hash, check_password_hash
from model import PostPunchRequest,PatchPunchRequest


app = Flask(__name__)
def db_init():
    db = pymysql.connect(
        host = 'ec2-34-208-156-155.us-west-2.compute.amazonaws.com',
        user = 'erp',
        password = 'erp',
        port = 3306
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor
class POST(Resource):
    @use_kwargs(PostPunchRequest)
    def post(self,**kwargs):
        db,cursor=db_init()
        po_number = kwargs.get("PO_Number")
        Account=kwargs.get("Account")
        Passwd = kwargs.get("Passwd")
        Team = kwargs.get("Team")
        Dept = kwargs.get("Dept")
        PO_Name = kwargs.get("PO_Name")

        password_new = generate_password_hash(Passwd)

        sql = """

        INSERT INTO `metaage_sales`.`me_IT` (`po_number`,`Email`,`Passwd`,`Team`,`Dept`,`PO_Name`)
        VALUES ('{}','{}','{}','{}','{}','{}');

        """.format(
            po_number,Account,password_new,Team, Dept, PO_Name)
        # result = cursor.execute(sql)
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return{
            'message': '01 成功',
            'po_number': po_number
          }
        except:
            cursor.close()
            db.close()
            return{
            'message': '00 失敗',
            'po_number': po_number
          }


class Delete(Resource):
    def delete(self,PO_Name):
        db, cursor = db_init()
        sql = """DELETE FROM `metaage_sales`.`me_IT` WHERE `me_IT`.`PO_Name` = '{}';""".format(PO_Name)

        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()
            return{
            'message': '01 成功',
            'PO_Name': PO_Name
          }
        except:
            cursor.close()
            db.close()
            return{
            'message': '00 失敗',
            'PO_Name': PO_Name
            }
        

        