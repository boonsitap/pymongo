import pymongo
from datetime import datetime,date
from flask import Flask,request
from flask_restful import Resource ,Api ,reqparse

client = pymongo.MongoClient('localhost',27017)
db = client.company

app= Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('firstname')
parser.add_argument('lastname')
parser.add_argument('employee_id')

office = db.office

class History(Resource):
        def get(self):
                args = parser.parse_args()
                id = args['id']
                info = office.find_one({"user.employee_id":id})
                if(info):
                        firstname = info['user']['firstname']
                        lastname = info['user']['lastname']
                        list_office = info['list_office']
                        return {"firstname":firstname,"lastname":lastname,"list_office":list_office}
                return {}
class Register(Resource):
        def post(self):
                args = parser.parse_args()
                id = args['employee_id']
                firstname = args['firstname']
                lastname = args['lastname']
                password = args['password']
                info = office.find_one({"user.employee_id":id})
                if(info):
                        return {"err":"System has this id"}
                office.insert({"user":{"employee_number":id,"firstname":firstname,"lastname":lastname,"password":password},"list_office":[]})
                return {"firstname":firstname,"lastname":lastname,"employee_id":id,"password":password}
class Login(Resource):
        def post(self):
                args = parser.parse_args()
                username = args['username']
                password = args['password']
                info = office.find_one({"user.employee_id":username,"user.password":password})
                if(info):
                        firstname = info['user']['firstname']
                        lastname = info['user']['lastname']
                        datetime_login = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        office.update({"user.employee_number":username},{"$push":{"list_office":{"datetime":datetime_login}}})
                        return {"firstname":firstname,"lastname":lastname,"datetime":datetime_login}
                return {}
api.add_resource(Register,'/api/register')
api.add_resource(Login,'/api/login')
api.add_resource(History,'/api/list_office')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)
