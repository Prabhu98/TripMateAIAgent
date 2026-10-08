import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

print("API key loaded:", bool(API_KEY))
print("API key length:", len(API_KEY) if API_KEY else 0)

BASE_URL = "https://api.aviationstack.com/v1/flights"


def search_flights(query, api_key=API_KEY):

    print("\n--- FUNCTION DEBUG ---")
    print("Function received API key:", bool(api_key))

    if not api_key:
        return "AviationStack API key is missing."

    print("Query:", query)

    match = re.search(
        r"from\s+(.+?)\s+to\s+(.+)",
        query.lower()
    )

    if not match:
        return "Could not determine origin and destination."

    origin = match.group(1).strip()
    destination = match.group(2).strip()

    print("Origin:", origin)
    print("Destination:", destination)

    airport_codes = {
        "chennai": "MAA",
        "tokyo": "NRT",
        "delhi": "DEL",
        "mumbai": "BOM",
        "dhaka": "DAC"
    }

    dep_iata = airport_codes.get(origin)
    arr_iata = airport_codes.get(destination)

    print("Departure IATA:", dep_iata)
    print("Arrival IATA:", arr_iata)

    if not dep_iata or not arr_iata:
        return "Unknown airport."

    response = requests.get(
        BASE_URL,
        params={
            "access_key": api_key,
            "dep_iata": dep_iata,
            "arr_iata": arr_iata
        },
        timeout=10
    )

    print("HTTP Status:", response.status_code)
    print("Response Body:", response.text)

    response.raise_for_status()

    return response.json()



search_query = "Plan a 7 days dhaka trip from delhi"
result = search_flights(search_query)
print("Search Result:", result)





