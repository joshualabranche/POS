#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 01:28:17 2024

@author: jlab
"""

#! /usr/bin/env python3.6
"""
server.py
Stripe Sample.
Python 3.7 or newer required.
"""

import stripe
import os
import json

from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

static_dir = str(os.path.abspath(os.path.join(os.getenv("STATIC_DIR"))))
app = Flask(__name__,
            static_folder=static_dir,
            static_url_path="",
            template_folder=static_dir)

order = [
    { "id": 1, "items":"plantains, jerk chicken", "customer": "John Doe", "total": 100.00 },
    { "id": 2, "items": "chicken sandwich, cheesy mac, gatorade", "customer": "Jane Smith", "total": 75.50 },
    { "id": 3, "items": "small fries", "customer": "Bob Johnson", "total": 210.25 }
]

@app.route("/", methods=['GET', 'PSOT'])
def home():
    return app.send_static_file('./html/orderDetails.html')


@app.route("/order", methods=['GET', 'PUT'])
def retrieve_order_info():
    if request.method == 'GET':          
        try:
            # do stuff to get data
            return jsonify(order)
        except Exception as e:
            return jsonify({"error": {"message": str(e)}})
    elif request.method == 'PUT':
        try:
            new_request = request.get_json()
            print(new_request)
            if "remove_order" in new_request.keys():
                count = -1
                for orders in order:
                    count += 1
                    if orders["id"]==new_request["remove_order"]:
                        order.pop(count)                   
            else:
                order.append(new_request)
            return jsonify(order)
        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)