import os

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
ORION_URL = os.getenv("ORION_URL", "http://orion:1026/v2/entities")
CITIES = ["NAT", "GRU"]

FLIGHT_DATE = os.getenv("FLIGHT_DATE", "2024-05-23")  # exemplo: 2024-05-23
IATA_CODE = os.getenv("AIRPORT_IATA", "NAT")
DIRECTION = os.getenv("DIRECTION", "departure")  # "departure" ou "arrival"
