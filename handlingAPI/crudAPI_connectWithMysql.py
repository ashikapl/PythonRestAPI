from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# connect mysql using pymysql
db = pymysql.connect(
    host="localhost",
    user="ashika",
    password="ashi",
    database="customers"
)


# create
