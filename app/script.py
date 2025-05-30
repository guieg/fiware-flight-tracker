import requests
import json

# from app.config import ORION_URL
ORION_URL = "http://localhost:1026/v2/entities"  # URL do Orion Context Broker
# ORION_URL = <ORION_URL>/orion/v2/entities"
HEADERS = {"Content-Type": "application/json"}

def create_flight_entity():
    data = {
        "id": "Flight:TEST123",
        "type": "Flight",
        "status": {
            "type": "Text",
            "value": "scheduled"
        }
    }
    response = requests.post(ORION_URL, headers=HEADERS, data=json.dumps(data))
    if response.status_code in [201, 204]:
        print("Entidade Flight criada com sucesso!")
    elif response.status_code == 422:
        print("Entidade já existe.")
    else:
        print(f"Erro ao criar entidade: {response.status_code}, {response.text}")

def update_flight_entity():
    entity_id = "Flight:TEST123"
    url = f"{ORION_URL}/{entity_id}/attrs"
    data = {
        "status": {
            "type": "Text",
            "value": "delayed"
        }
    }
    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))
    if response.status_code in [204]:
        print("Entidade Flight atualizada com sucesso!")
    else:
        print(f"Erro ao atualizar entidade: {response.status_code}, {response.text}")

if __name__ == "__main__":
    create_flight_entity()
    update_flight_entity()
