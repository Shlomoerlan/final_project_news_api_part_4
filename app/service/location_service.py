from dataclasses import dataclass
from typing import Optional
from geopy.geocoders import Nominatim
from app.db.models import Coordinates


@dataclass
class LocationService:
    _geocoder = Nominatim(user_agent="terror_analysis", timeout=10)

    @classmethod
    def get_coordinates(cls, city: str, country: str) -> Optional[Coordinates]:
        try:
            if not all([city, country]):
                return None

            location = cls._geocoder.geocode(f"{city}, {country}")

            if location:
                return Coordinates(
                    lat=location.latitude,
                    lon=location.longitude
                )
            return None

        except Exception as e:
            print(f"Error getting coordinates for {city}, {country}: {e}")
            return None