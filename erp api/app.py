from flask import Flask,request
from flask_restful import Api
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from main import *
from marshmallow import fields
from flask_apispec import use_kwargs

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True 


api.add_resource(POST, "/post")
api.add_resource(Delete, "/delete/<string:PO_Name>")


if __name__ == '__main__':
    app.run()
