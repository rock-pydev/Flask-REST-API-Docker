from flask import Flask, jsonify, render_template
import mysql.connector
from json_encoder import json
import statistics

app = Flask(__name__)


def getMysqlConnection():
    return mysql.connector.connect(user='root', host='db', port='3306', password='root', database='city')


def query_result(query, method):
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute(query)
    if method:
        data = cur.fetchall()
        return data
    else:
        return None

def statistics_values():
    query = 'SELECT Sell from cities'
    try:
        data = query_result(query, True)
        return {
            'mean': mean(data),
            'fmean': fmean(data),
            'geometric_mean': geometric_mean(data),
            'median': median(data),
            'median_low': median_low(data),
            'median_high': median_high(data),
            'median_grouped': median_grouped(data)
        }
    except Exception as e:
        return None

@app.route('/getCity', methods=['GET'])
def get_city():
    query = "SELECT * from cities"
    try:
        data = query_result(query, True)
        # data = cur.fetchall()
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
    except Exception as e:
        print(e)
        return jsonify({'caught': False})


@app.route('/addCity', methods=['POST'])
def add_city():
    query = "INSERT INTO cities \
             (Sell, List, Living, Rooms, Beds, Baths, Age, Acres, Taxes) \
             VALUES (142, 160, 28, 10, 5, 3, 60, 0.28, 3167);"
    try:
        query_result(query, False)
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
        query_result(query, False)
        return jsonify({"updated": True})
    except Exception as e:
        print(e)
        return jsonify({"updated": False})


@app.route('/deleteCity', methods=['DELETE'])
def delete_city():
    query = "DELETE FROM cities WHERE Sell=150;"
    try:
        query_result(query, False)
        return jsonify({"deleted": True})
    except Exception as e:
        print(e)
        return jsonify({"deleted": False})


@app.route('/statistics')
def statistics():
    return statistics_values()

@app.route('/')
@app.route('/login')
def login():
    return render_template('auth/login.html', current_user=None)

@app.route('/dashboard')
def dashboard():
    stat_vals = statistics_values()
    return render_template('home/index.html', stat_vals=stat_vals, current_user=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
