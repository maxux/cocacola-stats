import os
import sys
import pymysql
import hashlib
import uuid
from datetime import datetime
from flask import Flask, request, render_template, abort, g, redirect, jsonify
from config import config

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.url_map.strict_slashes = False

@app.context_processor
def inject_now():
    return {"now": datetime.utcnow()}

@app.before_request
def before_request_handler():
    g.db = pymysql.connect(
        host=config['db-server'],
        user=config['db-user'],
        password=config['db-pass'],
        database=config['db-name'],
        autocommit=True
    )

@app.route('/info', methods=['GET'])
def info():
    info = {
        "items": [],
        "consumers": [],
    }

    cursor = g.db.cursor()
    query = "SELECT id, name FROM consumers"
    cursor.execute(query)

    for row in cursor.fetchall():
        info["consumers"].append([row[0], row[1], 0])

    query = """
        SELECT cu.id, cu.name, COUNT(*)
        FROM consumers cu LEFT JOIN consumption co ON (co.consumer = cu.id)
        WHERE co.created > DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
        GROUP BY cu.id
    """
    cursor.execute(query)

    for row in cursor.fetchall():
        for consumer in info["consumers"]:
            if consumer[1] == row[1]:
                consumer[2] = row[2]

    query = "SELECT id, name, quantity FROM items"
    cursor.execute(query)

    for row in cursor.fetchall():
        info["items"].append(row)

    return jsonify(info)

@app.route('/consume/<consumer>/<item>', methods=['GET'])
def consome(consumer, item):
    cursor = g.db.cursor()
    query = "INSERT INTO consumption (created, consumer, item) VALUES (CURRENT_TIMESTAMP, %s, %s)"
    cursor.execute(query, (consumer, item))

    query = """
        SELECT COUNT(*)
        FROM consumers cu LEFT JOIN consumption co ON (co.consumer = cu.id)
        WHERE co.created > DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
          AND cu.id = %s
    """
    cursor.execute(query, (consumer))
    recent = cursor.fetchone()

    return jsonify({"status": "success", "recent": recent[0]})

@app.route('/summary', methods=['GET'])
def summary():
    cursor = g.db.cursor()
    query = """
        SELECT c.name, COUNT(*) qt, DATE(x.created) xday
        FROM `consumption` x, consumers c, items i
        WHERE c.id = x.consumer
        AND i.id = x.item
        GROUP BY xday, name
    """
    cursor.execute(query)
    response = []

    for row in cursor.fetchall():
        response.append(row)

    return jsonify(response)

@app.route('/', methods=['GET'])
def cocacola_index():
    return render_template("index.html")

def production():
    return app

if __name__ == '__main__':
    print("[+] listening into debug mode")
    app.run(host=config['listen'], port=config['port'], debug=config['debug'], threaded=True)

