from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        json = request.get_json()
        req_data = pd.DataFrame({
            'name': [json['name']],
            'age': [json['age']],
            'city': [json['city']]
        })
        data = pd.read_csv('users.csv')
        data = pd.concat([data, req_data], ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message': 'Kayıt başarıyla eklendi.'}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('users.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('users.csv', index=False)
            return {'message': 'Kayıt başarıyla silindi.'}, 200
        else:
            return {'message': 'Kayıt bulunamadı.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv', usecols=[2])
        data = data.to_dict('records')
        return {'data' : data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data' : entry}, 200
        return {'message' : 'Bu isimle bir giriş bulunamadı!'}, 404

class FilterByAge(Resource):
    def get(self, age_filter):
        data = pd.read_csv('users.csv')
        filtered_data = data[data['age'] > int(age_filter)]
        filtered_data = filtered_data.to_dict('records')
        return {'data': filtered_data}, 200

api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/<string:name>')
api.add_resource(FilterByAge, '/filter_by_age/<int:age_filter>')


