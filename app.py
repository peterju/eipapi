from flask import Flask, request
from flask_restful import Resource, Api
import pymssql

app = Flask(__name__)
api = Api(app)

class Member(Resource):
    def get(self, id=None):
        conn = pymssql.connect(
            server='your_server_name',
            database='your_database_name',
            user='your_username',
            password='your_password'
        )
        cursor = conn.cursor()
        if id:
            query = "SELECT * FROM members WHERE id=%s"
            cursor.execute(query, id)
        else:
            query = "SELECT * FROM members"
            cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
        return results

    def put(self, id):
        conn = pymssql.connect(
            server='your_server_name',
            database='your_database_name',
            user='your_username',
            password='your_password'
        )
        cursor = conn.cursor()
        query = "UPDATE members SET "
        data = request.get_json()
        for key in data:
            query += key + "='" + str(data[key]) + "',"
        query = query[:-1] + " WHERE id=%s"
        cursor.execute(query, id)
        conn.commit()
        conn.close()
        return {'message': 'Member data updated successfully.'}

api.add_resource(Member, '/members', '/members/<int:id>')
