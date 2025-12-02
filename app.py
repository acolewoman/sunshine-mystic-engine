from flask import Flask, request, jsonify
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.json

    date = data["date"]      # e.g., "1975-04-28"
    time = data["time"]      # e.g., "17:40"
    lat = float(data["lat"]) # numerical
    lon = float(data["lon"]) # numerical

    # Convert date/time into Flatlib format
    year, month, day = date.split("-")
    hour, minute = time.split(":")

    dt = Datetime(year, month, day, hour, minute, "+00:00")
    pos = GeoPos(lat, lon)

    # Build the chart
    chart = Chart(dt, pos)

    # Collect planetary info
    planets = {}
    for obj in chart.objects:
        planets[obj] = {
            "lon": chart[obj].lon,
            "lat": chart[obj].lat,
            "sign": chart[obj].sign,
            "house": chart[obj].house
        }

    # Houses
    houses = {}
    for house in chart.houses:
        houses[house] = chart.houses[house].cusplen

    return jsonify({
        "planets": planets,
        "houses": houses
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
