  from flask import Flask, request, jsonify
import swisseph as swe
import datetime

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    data = request.json

    date = data["date"]      # YYYY-MM-DD
    time = data["time"]      # HH:MM
    lat = float(data["lat"])
    lon = float(data["lon"])

    # Convert date & time to Julian Day
    year, month, day = map(int, date.split("-"))
    hour, minute = map(int, time.split(":"))
    jd = swe.julday(year, month, day, hour + minute/60)

    # Get planetary positions
    planets = {}
    for planet in range(swe.SUN, swe.PLUTO + 1):
        pos = swe.calc_ut(jd, planet)[0]
        planets[planet] = pos

    return jsonify({
        "julian_day": jd,
        "planets": planets
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
