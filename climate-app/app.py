from flask import Flask, jsonify
from climate_db import db, Measurement, Station
import datetime as dt
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hawaii.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    precipitation_data = db.session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precip_dict)

@app.route('/api/v1.0/stations')
def stations():
    stations = db.session.query(Station.station).all()
    station_list = [station[0] for station in stations]
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def temperature_observations():
    prev_year = dt.date.today() - dt.timedelta(days=365)
    most_active_station = db.session.query(Measurement.station, func.count(Measurement.station))\
                                  .group_by(Measurement.station)\
                                  .order_by(func.count(Measurement.station).desc())\
                                  .first()[0]
    temperature_data = db.session.query(Measurement.date, Measurement.tobs)\
                              .filter(Measurement.station == most_active_station)\
                              .filter(Measurement.date >= prev_year).all()
    temp_list = [temp[1] for temp in temperature_data]
    return jsonify(temp_list)

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats(start, end=None):
    if not end:
        end = dt.date.today().strftime('%Y-%m-%d')

    stats_data = db.session.query(func.min(Measurement.tobs), 
                               func.avg(Measurement.tobs), 
                               func.max(Measurement.tobs))\
                        .filter(Measurement.date >= start)\
                        .filter(Measurement.date <= end).all()

    stats_dict = {
        "TMIN": stats_data[0][0],
        "TAVG": stats_data[0][1],
        "TMAX": stats_data[0][2]
    }
    return jsonify(stats_dict)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
