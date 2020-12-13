from flask import Flask
import mysql.connector
from json_encoder import json

app = Flask(__name__)


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='db', port='3306', password='root', database='city')

def query_result(query):
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data


@app.route('/getCity', methods=['GET'])
def get_city():
    query = "SELECT * from cities"
    data = query_result(query)
    return json.dumps(data)


@app.route('/addCity', methods=['POST'])
def add_city():
    query = "INSERT INTO cities \
             (Sell, List, Living, Rooms, Beds, Baths, Age, Acres, Taxes) \
             VALUES (142, 160, 28, 10, 5, 3, 60, 0.28, 3167);"
    data = query_result(query)
    return json.dumps(data)


@app.route('/modifyCity', methods=['PUT'])
def modify_city():
    query = "UPDATE cities \
             SET Sell=150 \
             WHERE List = 160;"
    data = query_result(query)
    return json.dumps(data)


@app.route('/deleteCity', methods=['DELETE'])
def delete_city():
    query = "DELETE FROM Customers WHERE Sell=150;"
    data = query_result(query)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
