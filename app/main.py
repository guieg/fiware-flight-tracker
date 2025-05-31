from time import sleep
from fiware_client import fetch_flights, to_ngsi_entity, send_to_orion
from config import IATA_CODE, ORION_URL

flights = fetch_flights(IATA_CODE)
for flight in flights:
    entity = to_ngsi_entity(flight)
    # flight_num = flight.get("flight", {}).get("iataNumber", "UNKNOWN")
    print(entity)
    send_to_orion(entity)
    # print(f"Sent flight {flight_num} to Orion Context Broker.")

