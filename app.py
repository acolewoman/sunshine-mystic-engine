from flask import Flask, request, jsonify
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    # Get JSON payload
    data = request.get_json(force=True)

    # Expected input
    # {
    #   "date": "1975-04-28",
    #   "time": "17:40",
    #   "lat": 31.3220,
    #   "lon": -92.4340
    # }

    date = data["date"]
    time = data["time"]
    lat = float(data["lat"])
    lon = float(data["lon"])

    # Convert to Flatlib formats
    year, month, day = date.split("-")
    hour, minute = time.split(":")

    # Flatlib wants date like "YYYY/MM/DD" and time "HH:MM"
    dt = Datetime(f"{year}/{month}/{day}", f"{hour}:{minute}", "+00:00")
    pos = GeoPos(lat, lon)

    # Build the chart (default traditional objects, default house system)
    chart = Chart(dt, pos)

    # Collect planetary info
    planets = {}
    for obj in chart.objects:  # obj is a Flatlib object, not a string
        house = chart.houses.getObjectHouse(obj)
        planets[obj.id] = {
            "lon": obj.lon,
            "lat": obj.lat,
            "sign": obj.sign,
            "signlon": obj.signlon,
            "house": house.id if house else None
        }

    # Collect houses info
    houses = {}
    for house in chart.houses:  # house is a House object
        houses[house.id] = {
            "lon": house.lon,
            "sign": house.sign,
            "signlon": house.signlon,
            "size": house.size
        }

    return jsonify({
        "planets": planets,
        "houses": houses
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
