from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import pandas as pd
from app.db.models import Coordinates, DataSource, TerrorEvent
from app.service.location_service import LocationService


@dataclass
class CSVProcessor:
    @staticmethod
    def create_terror_event(
            title: str,
            content: str,
            date: datetime,
            location: str,
            coordinates: Optional[Coordinates],
            source: DataSource
    ) -> TerrorEvent:
        return TerrorEvent(
            title=title,
            content=content,
            publication_date=date,
            category="historic_terror",
            location=location,
            confidence=1.0,
            source_url=source.value,
            coordinates=coordinates
        )

    @classmethod
    def process_main_csv(cls, filepath: str, limit: int = None) -> List[TerrorEvent]:
        df = pd.read_csv(filepath, encoding='iso-8859-1')
        if limit:
            df = df.head(limit)
        events = []

        for _, row in df.iterrows():
            try:
                date = cls._parse_date(row['iyear'], row['imonth'], row['iday'])
                if not date:
                    continue

                coordinates = cls._extract_coordinates(row)
                location = f"{row['city']}, {row['country_txt']}"

                event = cls.create_terror_event(
                    title=f"Terror Attack in {location}",
                    content=cls._create_content(row),
                    date=date,
                    location=location,
                    coordinates=coordinates,
                    source=DataSource.MAIN_CSV
                )
                events.append(event)
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        return events

    @classmethod
    def process_secondary_csv(cls, filepath: str, limit: int = None) -> List[TerrorEvent]:
        df = pd.read_csv(filepath, encoding='iso-8859-1')
        if limit:
            df = df.head(limit)
        events = []

        for _, row in df.iterrows():
            try:
                date = datetime.strptime(row['Date'], '%d-%b-%y')
                location = f"{row['City']}, {row['Country']}"
                coordinates = LocationService.get_coordinates(row['City'], row['Country'])

                event = cls.create_terror_event(
                    title=f"Terror Attack in {location}",
                    content=cls._clean_text(row['Description']),
                    date=date,
                    location=location,
                    coordinates=coordinates,
                    source=DataSource.SECONDARY_CSV
                )
                events.append(event)
            except Exception as e:
                print(f"Error processing row from secondary CSV: {e}")
                continue

        return events

    @staticmethod
    def _parse_date(year: int, month: Optional[int], day: Optional[int]) -> Optional[datetime]:
        try:
            return datetime(
                year=int(year),
                month=int(month) if pd.notna(month) else 1,
                day=int(day) if pd.notna(day) else 1
            )
        except ValueError:
            return None

    @staticmethod
    def _extract_coordinates(row: pd.Series) -> Optional[Coordinates]:
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            return Coordinates(
                lat=float(row['latitude']),
                lon=float(row['longitude'])
            )
        return LocationService.get_coordinates(row['city'], row['country_txt'])

    @staticmethod
    def _clean_text(text: str) -> str:
        if pd.isna(text):
            return ""
        try:
            return str(text).strip()
        except:
            return ""

    @staticmethod
    def _create_content(row: pd.Series) -> str:
        if pd.notna(row.get('summary')):
            return CSVProcessor._clean_text(row['summary'])

        attack_type = CSVProcessor._clean_text(row.get('attacktype1_txt', ''))
        target_type = CSVProcessor._clean_text(row.get('targtype1_txt', ''))

        if attack_type and target_type:
            return f"{attack_type} attack targeting {target_type}"
        return "Terror incident"


# services/csv_processor.py
    @classmethod
    def test_csv_loading(cls, filepath: str, num_rows: int = 5) -> None:
        try:
            df = pd.read_csv(filepath, encoding='iso-8859-1', nrows=num_rows)
            print("\nTest CSV Loading Results:")
            print("-" * 50)
            print(f"Successfully loaded {len(df)} rows")
            print("\nColumns found:")
            for col in df.columns:
                print(f"- {col}")
            print("\nSample data from first row:")
            for col in df.columns:
                print(f"{col}: {df[col].iloc[0]}")

        except Exception as e:
            print(f"Error loading CSV: {e}")


    @classmethod
    def test_event_creation(cls, filepath: str, num_rows: int = 2) -> None:
        try:
            events = cls.process_main_csv(filepath, limit=num_rows)
            print("\nTest Event Creation Results:")
            print("-" * 50)
            for i, event in enumerate(events, 1):
                print(f"\nEvent {i}:")
                print(f"Title: {event.title}")
                print(f"Date: {event.publication_date}")
                print(f"Location: {event.location}")
                if event.coordinates:
                    print(f"Coordinates: lat={event.coordinates.lat}, lon={event.coordinates.lon}")
                print(f"Content preview: {event.content[:100]}...")

        except Exception as e:
            print(f"Error creating events: {e}")

    @classmethod
    def load_csv(cls, filepath: str, num_rows: int = None) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath, encoding='iso-8859-1', nrows=num_rows)
        except Exception as e:
            print(f"Error loading CSV {filepath}: {e}")
            raise