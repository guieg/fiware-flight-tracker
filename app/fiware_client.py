import requests
from config import ORION_URL, AVIATIONSTACK_API_KEY, FLIGHT_DATE, DIRECTION

import requests
import os
import json
from datetime import datetime


def fetch_flights(iata):
    response = requests.get("http://api.aviationstack.com/v1/timetable", params={
        "access_key": AVIATIONSTACK_API_KEY,
        "iataCode": iata,
        "flight_date": FLIGHT_DATE,
        "type": DIRECTION
    })
    data = response.json()
    return data.get('data', [])

def to_ngsi_entity(flight):

    flight_info = flight.get('flight', {})
    departure_info = flight.get('departure', {})
    arrival_info = flight.get('arrival', {})
    airline_info = flight.get('airline', {})

    iata_number = flight_info.get('iataNumber', 'UNKNOWN')
    scheduled_time = departure_info.get('scheduledTime', 'UNKNOWN_TIME')

    flight_id = f"Flight:{iata_number}_{scheduled_time[:10]}"
    
    return {
        "id": flight_id,
        "type": "Flight",
        "airline": {
            "type": "Text",
            "value": flight["airline"].get("name")
        },
        "departureAirport": {
            "type": "Text",
            "value": flight["departure"].get("iataCode")
        },
        "departureTime": {
            "type": "DateTime",
            "value": flight["departure"].get("scheduledTime")
        },
        "arrivalAirport": {
            "type": "Text",
            "value": flight["arrival"].get("iataCode")
        },
        "arrivalTime": {
            "type": "DateTime",
            "value": flight["arrival"].get("scheduledTime")
        },
        "status": {
            "type": "Text",
            "value": flight.get("status")
        },
        "delayed": {
            "type": "Boolean",
            "value": bool(flight["departure"].get("delay"))
        }
    }

def send_to_orion(entity):
    headers = {
        "Content-Type": "application/json",
        "Fiware-Service": "flights",
        "Fiware-ServicePath": "/flights"
    }
    response = requests.post(ORION_URL, headers=headers, data=json.dumps(entity))
    if response.status_code not in [200, 201, 204]:
        print(f"Erro ao enviar para Orion: {response.status_code}, {response.text}")


