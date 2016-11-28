import googlemaps
from datetime import datetime
from pprint import pprint
import polyline
import matplotlib.pyplot as plt
import os

api_key = os.environ['GOOGLE_MAPS_API_KEY']

gmaps = googlemaps.Client(key=api_key)

directions = gmaps.directions("Pilevej 10, 9000 Aalborg",
                              "Norgesgade 22, 9000 Aalborg",
                              mode="driving")

route = directions[0]['legs'][0]
coordinates = []
duration = route['duration']['value']
for step in route['steps']:
    pline = step['polyline']['points']
    coordinates.extend(polyline.decode(pline))

plt.plot([x for x, y in coordinates],[y for x, y in coordinates])
plt.show()
pprint(coordinates)
print("Delay", duration / len(coordinates))
