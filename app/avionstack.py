import requests
from config import AVIATIONSTACK_API_KEY

def get_airport_flights(city):
    url = f"http://api.aviationstack.com/v1/flights"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": city,  # para buscar partidas
        "arr_iata": city,  # para buscar chegadas
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Erro na API da Aviationstack: {response.text}")
        return []
