#!/usr/bin/env python3
import begin
from faker import Factory
from urllib.parse import urljoin
import requests
from pprint import pprint
import gpxpy
import time

fake = Factory.create('en_US')
base_path = "/services-1.0.0"

def make_new_user(server, superuser):
    su_auth_header = authenticate_user(server, superuser)
    user_data = {
            "username" : fake.user_name(),
            "givenname": fake.first_name(),
            "surname"  : "McTestface",
            "password" : "hunter2"
    }

    r = requests.post(server + '/user', json=user_data, headers=su_auth_header)
    pprint(r.json())
    return r.json()['username'], "hunter2"

def authenticate_user(server, user):
    user_data = {"username": user[0], "password": user[1]}
    r = requests.post(server + '/auth', json=user_data)
    pprint(r.json())
    return {"Authorization": "Sleepy token=" + r.json()['token']}

def make_vehicle(server, auth_header):
    car_data = {
            "make" : fake.company(),
            "model" : fake.word(),
            "vintage" : fake.year(),
            "vin" : fake.ean13()
    }
    r = requests.post(server + '/vehicle', json=car_data, headers=auth_header)
    pprint(r.json())
    return r.json()['id']

def make_route(server, auth_header, vehicle_id):
    route_data = { "vehicleid": vehicle_id }
    r = requests.post(server + '/route', json=route_data, headers=auth_header)
    pprint(r.json())
    return r.json()['id']

def load_gpx_data(waypoints):
    with open(waypoints, 'r') as f:
        return gpxpy.parse(f)

def make_waypoint(server, auth_header, route_id, latitude, longitude):
    waypoint_data = {
            "latitude" : latitude,
            "longitude": longitude,
            "timestamp": int(time.time() * 1000)
    }
    r = requests.post(server + '/route/' + route_id + '/waypoint', json=waypoint_data, headers=auth_header)
    pprint(r.json())

@begin.start
def main(server: 'URL of the server' = "http://172.25.11.114:8080",
         user: 'If not supplied a new user will be made' = (None, None),
         superuser: 'Used to make new user' = ("deadpool", "hunter2"),
         waypoints: 'GPX file to read waypoints from' = "waypoints.gpx",
         waypoint_delay: 'Delay between POSTing waypoints' = 1):
    server = urljoin(server, base_path)
    print(server)
    if user[0] is None:
        user = make_new_user(server, superuser)
    auth_header = authenticate_user(server, user)
    vehicle_id = make_vehicle(server, auth_header)
    route_id = make_route(server, auth_header, vehicle_id)
    gpx = load_gpx_data(waypoints)
    for segment in gpx.tracks[0].segments:
        for point in segment.points:
            make_waypoint(server, auth_header, route_id, point.latitude, point.longitude)
            time.sleep(waypoint_delay)


