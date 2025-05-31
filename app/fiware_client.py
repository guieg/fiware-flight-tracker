import requests
from config import ORION_URL, AVIATIONSTACK_API_KEY, FLIGHT_DATE, DIRECTION, ORION_BASE_URL
import random

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

from hashlib import md5

def generate_flight_id(flight):
    flight_number = flight.get('flight', {}).get('iataNumber', 'UNKNOWN')
    departure_time = flight.get('departure', {}).get('scheduledTime', '1970-01-01T00:00:00Z')
    raw_id = f"{flight_number}_{departure_time}"
    return md5(raw_id.encode()).hexdigest()  # ou use diretamente raw_id


def to_ngsi_entity(flight):
    flight_info = flight.get('flight', {})
    departure_info = flight.get('departure', {})
    arrival_info = flight.get('arrival', {})
    airline_info = flight.get('airline', {})

    iata_number = flight_info.get('iataNumber', 'UNKNOWN')
    scheduled_time = departure_info.get('scheduledTime')

    if not scheduled_time:
        scheduled_time = "1970-01-01T00:00:00Z"  # fallback válido

    flight_id = generate_flight_id(flight)
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

    # Verifica se a entidade existe
    check = requests.get(f"{ORION_BASE_URL}/entities/{entity_id}", headers=headers_get)
    
    if check.status_code == 404:
        print(f"Criando nova entidade: {entity_id}")
        response = requests.post(f"{ORION_BASE_URL}/entities", headers=headers, data=json.dumps(entity))
    else:
        print(f"Atualizando entidade existente: {entity_id}")
        response = requests.patch(f"{ORION_BASE_URL}/entities/{entity_id}/attrs", headers=headers, data=json.dumps(entity_attrs))

    if response.status_code not in [200, 201, 204]:
        print(f"Erro ao enviar para Orion: {response.status_code}, {response.text}")