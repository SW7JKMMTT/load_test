#!/usr/bin/env python3
from pymongo import MongoClient

client = MongoClient('172.25.11.114', 27017)
db = client.test

print("Deleted", db.Driver.delete_many({}).deleted_count, "drivers")
print("Deleted", db.AuthToken.delete_many({}).deleted_count, "auth tokens")
print("Deleted", db.User.delete_many({"surname":"McTestface"}).deleted_count, "users")
print("Deleted", db.Permission.delete_many({"permission": "User"}).deleted_count, "user permissions")
print("Remove auth tokens from Wade Wilson")
db.User.update_one({"username":"deadpool"}, {"$set": {"authTokens": []}})
print("Deleted", db.Route.delete_many({}).deleted_count, "routes")
print("Deleted", db.Waypoint.delete_many({}).deleted_count, "waypoints")
print("Deleted", db.Vehicle.delete_many({}).deleted_count, "vehicles")
print("Done")
