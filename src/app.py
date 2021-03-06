from flask import Flask, jsonify, request, make_response
from src.api_handler import APIHandler

app = Flask(__name__)

handler = APIHandler()

@app.route("/api/<user>/transaction", methods=["POST"])
def create_transaction(user):
    payer = request.json['payer']
    points = int(request.json['points'])
    timestamp = request.json['timestamp']
    return handler.create_transaction(user, payer, points, timestamp)
        

@app.route("/api/<user>/create", methods=["POST"])
def create_user(user):
    return handler.create_user(user)

@app.route("/api/<user>/spend", methods=["PUT"])
def spend_points(user):
    points = int(request.json['points'])
    if points <= 0:
        return make_response(jsonify(response='Points must be positive', success=False), 400)
    
    return handler.spend_points(user, points)


@app.route("/api/<user>/points", methods=["GET"])
def get_points(user):
    itemized = int(request.args.get("itemized", 0))
    return handler.get_points(user) if itemized else handler.get_total_points(user)

