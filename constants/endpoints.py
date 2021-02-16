from resources import AirlineList, Airline
from resources import Aircraft, AircraftList
from resources import Airport, AirportByCountry, AirportList

AIRCRAFT = (Aircraft, "/aircraft/<string:brand>")
AIRCRAFTS = (AircraftList, "/aircrafts")

AIRLINE = (Airline, "/airline/<string:name>")
AIRLINES = (AirlineList, "/airlines")

AIRPORT = (Airport, "/airport/<string:iata>")
AIRPORT_BY_COUNTRY = (AirportByCountry, "/airports/<string:country>")
AIRPORTS = (AirportList, "/airports")
