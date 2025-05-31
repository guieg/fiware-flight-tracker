import requests
import json

# Configurações do Orion e QuantumLeap
ORION_URL = "http://localhost:1026/v2/subscriptions"  # Corrigido: sem /orion
NOTIFICATION_URL = "http://quantumleap:8668/v2/notify"  # Corrigido: endpoint correto

# Cabeçalhos HTTP
headers = {
    "Content-Type": "application/json",
    "Fiware-Service": "flights",
    "Fiware-ServicePath": "/flights" 
}

# Corpo da subscription
subscription = {
    "description": "Flight data to QuantumLeap",
    "subject": {
        "entities": [
            {
                "idPattern": ".*",
                "type": "Flight"
            }
        ]
    },
    "notification": {
        "http": {
            "url": NOTIFICATION_URL
        },
        "attrsFormat": "normalized"
    },
    "throttling": 1
}

# Envio da requisição
response = requests.post(ORION_URL, headers=headers, data=json.dumps(subscription))

# Verificação da resposta
if response.status_code in [201, 204]:
    print("✅ Subscription criada com sucesso!")
else:
    print(f"❌ Erro ao criar subscription: {response.status_code}")
    print(response.text)