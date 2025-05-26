# CrewAI Tools for Travel Agents
# Create these tools and assign them to your tasks

from crewai_tools import BaseTool
import requests
import json
from typing import Dict, List, Any
from pydantic import BaseModel, Field

# WEATHER TOOL - for Transportation Strategist
class WeatherForecastTool(BaseTool):
    name: str = "Weather Forecast Tool"
    description: str = "Get weather forecasts for destinations during travel dates. Use this to check for severe weather that might affect transportation."
    
    def _run(self, destinations: str, travel_dates: str) -> str:
        """
        Get weather forecast for destinations during travel period
        Args:
            destinations: Comma-separated list of destinations (e.g., "Tokyo, Bangkok")
            travel_dates: Travel period (e.g., "2024-03-15 to 2024-03-30")
        """
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your API key
        weather_data = {}
        
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            try:
                url = f"http://api.openweathermap.org/data/2.5/forecast"
                params = {
                    'q': destination,
                    'appid': api_key,
                    'units': 'metric'
                }
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    weather_data[destination] = {
                        'forecast_summary': f"5-day forecast for {destination}",
                        'severe_weather_alerts': self._check_severe_weather(data),
                        'average_temp': self._get_avg_temp(data)
                    }
                else:
                    weather_data[destination] = {'error': 'Weather data unavailable'}
                    
            except Exception as e:
                weather_data[destination] = {'error': str(e)}
        
        return json.dumps(weather_data, indent=2)
    
    def _check_severe_weather(self, data):
        alerts = []
        for forecast in data.get('list', [])[:10]:  # Next 5 days
            weather_main = forecast.get('weather', [{}])[0].get('main', '')
            if weather_main in ['Thunderstorm', 'Snow', 'Extreme']:
                alerts.append({
                    'date': forecast.get('dt_txt'),
                    'condition': weather_main,
                    'description': forecast.get('weather', [{}])[0].get('description')
                })
        return alerts
    
    def _get_avg_temp(self, data):
        temps = [item['main']['temp'] for item in data.get('list', [])[:10]]
        return sum(temps) / len(temps) if temps else 0

# VISA REQUIREMENTS TOOL - for Transportation Strategist
class VisaRequirementsTool(BaseTool):
    name: str = "Visa Requirements Tool"
    description: str = "Check visa requirements for a passport country traveling to specific destinations."
    
    def _run(self, passport_country: str, destinations: str) -> str:
        """
        Check visa requirements
        Args:
            passport_country: Country of passport (e.g., "United States")
            destinations: Comma-separated destinations (e.g., "Japan, Thailand")
        """
        # Using REST Countries API (free) as example
        visa_info = {}
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            try:
                # This is a simplified example - you'd use a proper visa API like Sherpa
                url = f"https://restcountries.com/v3.1/name/{destination}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()[0]
                    visa_info[destination] = {
                        'country_code': data.get('cca3', 'Unknown'),
                        'visa_policy': f"Check official sources for {passport_country} to {destination} visa requirements",
                        'embassy_info': data.get('capital', ['Unknown'])[0] if data.get('capital') else 'Unknown'
                    }
                else:
                    visa_info[destination] = {'error': 'Country data unavailable'}
                    
            except Exception as e:
                visa_info[destination] = {'error': str(e)}
        
        return json.dumps(visa_info, indent=2)

# CULTURAL EVENTS TOOL - for Cultural Experience Curator
class CulturalEventsTool(BaseTool):
    name: str = "Cultural Events Tool"
    description: str = "Find cultural events, festivals, and local experiences during travel dates."
    
    def _run(self, destinations: str, travel_dates: str, cultural_interest: str = "moderate") -> str:
        """
        Find cultural events during travel period
        Args:
            destinations: Comma-separated destinations
            travel_dates: Travel period (e.g., "2024-03-15 to 2024-03-30") 
            cultural_interest: Level of cultural interest (high/moderate/casual)
        """
        # Using Eventbrite API example
        api_key = "YOUR_EVENTBRITE_API_KEY"  # Replace with your API key
        events_data = {}
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            try:
                url = "https://www.eventbriteapi.com/v3/events/search/"
                headers = {'Authorization': f'Bearer {api_key}'}
                
                params = {
                    'location.address': destination,
                    'categories': '103,105,113',  # Arts, Business, Community
                    'sort_by': 'relevance'
                }
                
                # For demo purposes, using a mock response
                events_data[destination] = {
                    'cultural_events': [
                        {
                            'name': f'Cultural Festival in {destination}',
                            'date': 'Check local calendar',
                            'type': 'Traditional Arts',
                            'description': f'Local cultural experience in {destination}'
                        }
                    ],
                    'recommendations': f'Search for traditional festivals and cultural centers in {destination} during your travel dates'
                }
                    
            except Exception as e:
                events_data[destination] = {'error': str(e)}
        
        return json.dumps(events_data, indent=2)

# TRAVEL ADVISORIES TOOL - for Crisis Management Specialist  
class TravelAdvisoresTool(BaseTool):
    name: str = "Travel Advisories Tool"
    description: str = "Get current travel advisories, safety information, and risk assessments for destinations."
    
    def _run(self, destinations: str) -> str:
        """
        Get travel advisories and safety information
        Args:
            destinations: Comma-separated destinations
        """
        advisory_data = {}
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            try:
                # Using REST Countries for basic info (replace with proper travel advisory API)
                url = f"https://restcountries.com/v3.1/name/{destination}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()[0]
                    advisory_data[destination] = {
                        'country': data.get('name', {}).get('common', destination),
                        'region': data.get('region', 'Unknown'),
                        'safety_recommendation': f'Check current US State Department travel advisories for {destination}',
                        'emergency_numbers': 'Contact local emergency services: 911 equivalent',
                        'embassy_contact': f'Contact {destination} embassy for current safety information'
                    }
                else:
                    advisory_data[destination] = {'error': 'Advisory data unavailable'}
                    
            except Exception as e:
                advisory_data[destination] = {'error': str(e)}
        
        return json.dumps(advisory_data, indent=2)

# FLIGHT PRICING TOOL - for Intelligence Analyst
class FlightPricingTool(BaseTool):
    name: str = "Flight Pricing Tool" 
    description: str = "Get current flight prices and deals for destinations."
    
    def _run(self, origin: str, destinations: str, travel_dates: str) -> str:
        """
        Get flight pricing information
        Args:
            origin: Origin city/airport
            destinations: Comma-separated destinations
            travel_dates: Travel dates
        """
        # This would use Amadeus, Skyscanner API etc.
        # For demo, providing mock structure
        flight_data = {}
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            flight_data[destination] = {
                'route': f'{origin} to {destination}',
                'price_range': '$800 - $1500 (example)',
                'best_booking_time': '6-8 weeks in advance',
                'price_trend': 'Stable',
                'recommendations': f'Check Skyscanner, Expedia, and airline direct for {origin} to {destination} flights'
            }
        
        return json.dumps(flight_data, indent=2)

# HOTEL PRICING TOOL - for Intelligence Analyst
class HotelPricingTool(BaseTool):
    name: str = "Hotel Pricing Tool"
    description: str = "Get current hotel prices and accommodation deals."
    
    def _run(self, destinations: str, travel_dates: str, budget_range: str) -> str:
        """
        Get hotel pricing information
        Args:
            destinations: Comma-separated destinations
            travel_dates: Travel dates
            budget_range: Budget range (budget/mid-range/luxury)
        """
        # Would use Booking.com API, Hotels.com API etc.
        hotel_data = {}
        dest_list = [d.strip() for d in destinations.split(',')]
        
        for destination in dest_list:
            hotel_data[destination] = {
                'budget_options': f'$30-80/night in {destination}',
                'mid_range_options': f'$80-200/night in {destination}', 
                'luxury_options': f'$200+/night in {destination}',
                'booking_recommendations': f'Check Booking.com, Airbnb, and local hotels in {destination}',
                'best_areas': f'City center and tourist districts in {destination}'
            }
        
        return json.dumps(hotel_data, indent=2)

# Tool instances to use in your tasks
weather_tool = WeatherForecastTool()
visa_tool = VisaRequirementsTool()
events_tool = CulturalEventsTool()
advisories_tool = TravelAdvisoresTool()
flight_pricing_tool = FlightPricingTool()
hotel_pricing_tool = HotelPricingTool()

