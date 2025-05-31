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
    scheduled_time = departure_info.get('scheduledTime')

    if not scheduled_time:
        scheduled_time = "1970-01-01T00:00:00Z"  # fallback válido

    flight_id = f"Flight:{iata_number}_{scheduled_time[:10]}"
    print(f"Processing flight ID: {flight_id}")
    
    return {
        "id": flight_id,
        "type": "Flight",  # Corrigido para começar com maiúscula
        "airline": {
            "type": "Text",
            "value": airline_info.get("name", "Unknown")
        },
        "departureAirport": {
            "type": "Text",
            "value": departure_info.get("iataCode", "Unknown")
        },
        "departureTime": {
            "type": "DateTime",
            "value": scheduled_time
        },
        "arrivalAirport": {
            "type": "Text",
            "value": arrival_info.get("iataCode", "Unknown")
        },
        "arrivalTime": {
            "type": "DateTime",
            "value": arrival_info.get("scheduledTime", "1970-01-01T00:00:00Z")
        },
        "status": {
            "type": "Text",
            "value": flight.get("status", "unknown")
        },
        "delayed": {
            "type": "Boolean",
            "value": bool(departure_info.get("delay", 0))
        }
    }
   

def send_to_orion(entity):
    headers_get = {
        "Fiware-Service": "flights",
        "Fiware-ServicePath": "/flights"
    }

    headers = {
        "Content-Type": "application/json",
        "Fiware-Service": "flights",
        "Fiware-ServicePath": "/flights"
    }


    entity_id = entity["id"]
    entity_attrs = entity.copy()
    entity_attrs.pop("id")
    entity_attrs.pop("type")
    
    print(ORION_URL)
    # Verifica se existe
    check = requests.get(f"{ORION_URL}/{entity_id}", headers=headers_get)
    if check.status_code == 404:
        # Criar nova entidade
        response = requests.post(ORION_URL, headers=headers, data=json.dumps(entity))
        print(response.text) 
    else:
        # Atualizar entidade existente (sem id/type no corpo)
        response = requests.patch(f"{ORION_URL}/{entity_id}/attrs", headers=headers, data=json.dumps(entity_attrs))

    if response.status_code not in [200, 201, 204]:
        print(f"Erro ao enviar para Orion: {response.status_code}, {response.text}")