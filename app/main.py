from config import CITIES, FLIGHT_DATE
# from aviationstack import get_airport_flights
from fiware_client import fetch_flights, to_ngsi_entity, send_to_orion

def main():
    for city in CITIES:
        print(f"🔍 Consultando voos para {city}")
        flights = fetch_flights(city)
        for flight in flights:
            entidade = to_ngsi_entity(flight)
            send_to_orion(entidade)
            print(f"Enviado: {entidade['id']}")
            print(f"✅ Publicado voo {flight.get('flight', {}).get('iata')}")

if __name__ == "__main__":
    main()

