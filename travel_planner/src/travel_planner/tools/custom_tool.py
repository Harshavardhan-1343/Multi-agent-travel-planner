from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Mapping city names to IATA codes
city_to_iata = {
    "bangalore": "BLR",
    "delhi": "DEL",
    "mumbai": "BOM",
    "chennai": "MAA",
    "hyderabad": "HYD",
    "kolkata": "CCU",
    "goa": "GOI",
    "kochi": "COK",
    "jaipur": "JAI",
}

# Input schema
class FlightSearchInput(BaseModel):
    """User query about flight search"""
    query: str = Field(..., description="User's query, like 'Flights from Bangalore to Delhi'")

# Tool class
class RealTimeFlightTool(BaseTool):
    name: str = "Real-Time Flight Search Tool"
    description: str = "Searches real-time flights between two cities mentioned in a query."
    args_schema: Type[BaseModel] = FlightSearchInput

    def _run(self, query: str) -> str:
        query = query.lower()
        from_city_match = re.search(r"from (\w+)", query)
        to_city_match = re.search(r"to (\w+)", query)

        if not from_city_match or not to_city_match:
            return "Could not extract 'from' and 'to' cities. Try saying: 'Find flights from Mumbai to Goa'."

        from_city = from_city_match.group(1)
        to_city = to_city_match.group(1)

        dep_iata = city_to_iata.get(from_city)
        arr_iata = city_to_iata.get(to_city)

        if not dep_iata or not arr_iata:
            return f"City not supported: {from_city if not dep_iata else to_city}. Try a major Indian city."

        api_key = os.getenv("AVIATIONSTACK_API_KEY")
        if not api_key:
            return "API key is missing. Please check your .env file."

        url = "http://api.aviationstack.com/v1/flights"
        params = {
            "access_key": api_key,
            "dep_iata": dep_iata,
            "arr_iata": arr_iata,
            "limit": 3
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"

        flights = response.json().get("data", [])
        if not flights:
            return "No flights found for this route right now."

        result = []
        for f in flights:
            airline = f['airline']['name']
            flight_no = f['flight']['iata']
            status = f['flight_status']
            result.append(f"{airline} {flight_no} - Status: {status}")

        return "\n".join(result)
