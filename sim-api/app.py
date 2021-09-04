import os
from flask import Flask, jsonify
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(host=os.getenv('DB_HOST'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASSWORD'),
                             database=os.getenv('DB_NAME'),
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/devices/<deviceId>/maxTemp', methods=['GET'])
def maxTemp(deviceId):
    sql = "SELECT deviceId, MAX(temperature) as max_temperature FROM Device WHERE deviceId = %s GROUP BY deviceId"
    cursor.execute(sql, (deviceId))
    result = cursor.fetchall()
    connection.commit()
    return jsonify({'data': result})

@app.route('/api/devices/<deviceId>/count', methods=['GET'])
def count(deviceId):
    sql = "SELECT deviceId, Count(*) as count FROM Device WHERE deviceId = %s GROUP BY deviceId"
    cursor.execute(sql, (deviceId))
    result = cursor.fetchall()
    connection.commit()
    return jsonify({'data': result})

@app.route('/api/devices/<deviceId>/maxTempPerDay', methods=['GET'])
def maxTempPerDay(deviceId):
    sql = "SELECT deviceId, DATE(from_unixtime(time)) as day_created, MAX(temperature) as max_temperature FROM Device WHERE deviceId = %s GROUP BY deviceId, day_created"
    cursor.execute(sql, (deviceId))
    result = cursor.fetchall()
    connection.commit()
    return jsonify({'data': result})