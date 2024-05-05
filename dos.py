from flask import Flask, current_app, request, make_response
from datetime import datetime, timedelta

from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312-project"]
ip_collection = db['ip_collection']


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


def DOS_prevention(cost):
    ip = request.headers['X-Real-IP']
    current_app.logger.info(ip)
    ip_found = find_ip_user(ip)
    current_time = int(round(datetime.now().timestamp()))
    if not ip_found:
        ip_collection.insert_one({"ip": ip, "count": cost, "time": current_time})
        # current_app.logger.info("RECORD CREATED")
    if ip_found:
        user = ip_collection.find({"ip": ip})[0]
        count = user["count"]
        current_app.logger.info(count)
        banned = not count
        if not banned:
            current_app.logger.info(current_time - user["time"])
            if user["count"] >= 50 and (current_time - user["time"]) <= 10:
                ip_collection.update_one({"ip": ip}, {"$set": {"count": 0}})
                ip_collection.update_one({"ip": ip}, {"$set": {"time": current_time}})
                # current_app.logger.info("BANNED!!!")
                return too_many_request()
            elif user["count"] < 50 and (current_time - user["time"]) > 10:
                # current_app.logger.info(current_time - user["time"])
                ip_collection.delete_one({"ip": ip})
                # current_app.logger.info("RECORD DELETED")
            else:
                ip_collection.update_one({"ip": ip}, {"$set": {"count": count + cost}})
        if banned:
            if (current_time - user["time"]) < 30:
                return too_many_request()
            if (current_time - user["time"]) >= 30:
                ip_collection.delete_one({"ip": ip})
