from resources import AirlineList, Airline
from resources import Aircraft, AircraftList

AIRCRAFT = (Aircraft, "/aircraft/<string:brand>")
AIRCRAFTS = (AircraftList, "/aircrafts")

AIRLINE = (Airline, "/airline/<string:name>")
AIRLINES = (AirlineList, "/airlines")
