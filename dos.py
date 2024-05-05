from flask import Flask, current_app, request, make_response
from datetime import datetime, timedelta

from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312-project"]
ip_collection = db['ip_collection']
TA_collection = db['TA_collection']

def find_ip_user(ip_address):
    if ip_collection.find_one({"ip": ip_address}) is not None:
        return True
    else:
        return False


def too_many_request():
    response = make_response("Too many requests")
    response.status_code = 429
    response.content_type = "text/plain"
    return response

def cost_ta_page() -> int:
    ta_users = TA_collection.find({})
    users = 0
    for single_ta in ta_users:
        users += 1
    return users

def DOS_prevention():
    cost = 0
    if request.path == '/':
        cost = 20
    if request.path == '/user':
        cost = 5
    if request.path == '/ta':
        cost = cost_ta_page() + 3
    ip = request.headers['X-Real-IP']
    ip_found = find_ip_user(ip)
    current_time = int(round(datetime.now().timestamp()))
    if not ip_found:
        current_app.logger.info("IP ADDRESS:")
        current_app.logger.info(ip)
        current_app.logger.info("Requests Called when created: ")
        current_app.logger.info(cost)
        current_app.logger.info("Time Duration:")
        current_app.logger.info(current_time)
        ip_collection.insert_one({"ip": ip, "count": cost, "time": current_time})
    if ip_found:
        user = ip_collection.find({"ip": ip})[0]
        count = user["count"]
        current_app.logger.info("IP ADDRESS:")
        current_app.logger.info(ip)
        current_app.logger.info("Requests Called if ip found: ")
        current_app.logger.info(count)
        current_app.logger.info("Time Duration:")
        current_app.logger.info(current_time - user["time"])
        banned = not count
        if not banned:
            if user["count"] >= 50 and (current_time - user["time"]) <= 10:
                ip_collection.update_one({"ip": ip}, {"$set": {"count": 0}})
                ip_collection.update_one({"ip": ip}, {"$set": {"time": current_time}})
                # current_app.logger.info("BANNED!!!")
                return too_many_request()
            elif user["count"] < 50 and (current_time - user["time"]) < 10:
                ip_collection.update_one({"ip": ip}, {"$set": {"count": count + cost}})
            else:
                ip_collection.delete_one({"ip": ip})
        if banned:
            if (current_time - user["time"]) < 30:
                return too_many_request()
            if (current_time - user["time"]) >= 30:
                ip_collection.delete_one({"ip": ip})
