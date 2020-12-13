from flask import Flask, jsonify
import mysql.connector
from json_encoder import json

app = Flask(__name__)


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='db', port='3306', password='root', database='city')


def query_result(query):
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute(query)
    return cur


@app.route('/getCity', methods=['GET'])
def get_city():
    query = "SELECT * from cities"
    cur = query_result(query)
    data = cur.fetchall()
    result = []
    for item in data:
        result.append({
            'Sell': item[0],
            'List': item[1],
            'Living': item[2],
            'Rooms': item[3],
            'Beds': item[4],
            'Baths': item[5],
            'Age': item[6],
            'Acres': item[7],
            'Taxes': item[8]
        })
    return json.dumps(result)


@app.route('/addCity', methods=['POST'])
def add_city():
    query = "INSERT INTO cities \
             (Sell, List, Living, Rooms, Beds, Baths, Age, Acres, Taxes) \
             VALUES (142, 160, 28, 10, 5, 3, 60, 0.28, 3167);"
    try:
        query_result(query)
        return jsonify({"added": True})
    except Exception as e:
        print(e)
        return jsonify({"added": False})


@app.route('/modifyCity', methods=['PUT'])
def modify_city():
    query = "UPDATE cities \
             SET Sell=150 \
             WHERE List = 160;"
    try:
        query_result(query)
        return jsonify({"updated": True})
    except Exception as e:
        print(e)
        return jsonify({"updated": False})


@app.route('/deleteCity', methods=['DELETE'])
def delete_city():
    query = "DELETE FROM Customers WHERE Sell=150;"
    try:
        query_result(query)
        return jsonify({"deleted": True})
    except Exception as e:
        print(e)
        return jsonify({"deleted": False})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
