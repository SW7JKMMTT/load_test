#!/usr/bin/env python3
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('172.25.11.114', 27017)
db = client.test

test_userids = []
for user in db.User.find({"surname": "McTestface"}):
    test_userids.append(user['_id'])

print('Deleted', db.User.delete_many({"_id" : {"$in" : test_userids}}).deleted_count, "users")
print('Deleted', db.Permission.delete_many({"user_id" : {"$in" : test_userids}}).deleted_count, "permisisons")
print('Deleted', db.AuthToken.delete_many({"user_id" : {"$in" : test_userids}}).deleted_count, "auth tokens")

test_driverids = []
for driver in db.Driver.find({"user_id": {"$in" : test_userids}}):
    test_driverids.append(driver['_id'])

print('Deleted', db.Driver.delete_many({"_id": {"$in" : test_driverids}}).deleted_count, "drivers")

test_routeids = []
test_vehicleids = []
for route in db.Route.find({"driver_id": {"$in" : test_driverids}}):
    test_routeids.append(route['_id'])
    test_vehicleids.append(route['vehicle_id'])

print('Deleted', db.Route.delete_many({"_id": {"$in" : test_routeids}}).deleted_count, "routes")
print('Deleted', db.Waypoint.delete_many({"route_id": {"$in" : test_routeids}}).deleted_count, "waypoints")
print('Deleted', db.Vehicle.delete_many({"_id": {"$in" : test_vehicleids}}).deleted_count, "vehicles")

print("Cleaning deadpool")
su_id = db.User.find_one_and_update({"username":"deadpool"}, {"$set": {"authTokens": []}})['_id']
print('Deleted', db.AuthToken.delete_many({"user_id" : su_id}).deleted_count, "su auth tokens")

print("Done")
