import requests
from config import ORION_URL, AVIATIONSTACK_API_KEY, FLIGHT_DATE, DIRECTION

import json

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
            "value": airline_info.get("name")
        },
        "departureAirport": {
            "type": "Text",
            "value": departure_info.get("iataCode")
        },
        "departureTime": {
            "type": "DateTime",
            "value": departure_info.get("scheduledTime")
        },
        "arrivalAirport": {
            "type": "Text",
            "value": arrival_info.get("iataCode")
        },
        "arrivalTime": {
            "type": "DateTime",
            "value": arrival_info.get("scheduledTime")
        },
        "status": {
            "type": "Text",
            "value": flight.get("status")
        },
        "delayed": {
            "type": "Boolean",
            "value": bool(departure_info.get("delay"))
        }
    }

def send_to_orion(entity):
    headers = {
        "Content-Type": "application/json",
        "Fiware-Service": "flights",
        "Fiware-ServicePath": "/flights"
    }

    entity_id = entity["id"]
    entity_attrs = entity.copy()
    entity_attrs.pop("id")
    entity_attrs.pop("type")

    # Verifica se existe
    check = requests.get(f"{ORION_URL}/{entity_id}", headers=headers)

    if check.status_code == 404:
        # Criar nova entidade
        response = requests.post(ORION_URL, headers=headers, data=json.dumps(entity))
    else:
        # Atualizar entidade existente (sem id/type no corpo)
        response = requests.patch(f"{ORION_URL}/{entity_id}/attrs", headers=headers, data=json.dumps(entity_attrs))

    if response.status_code not in [200, 201, 204]:
        print(f"Erro ao enviar para Orion: {response.status_code}, {response.text}")
