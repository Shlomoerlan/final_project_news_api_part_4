# tests/test_csv_loading.py
import pytest
from app.service.csv_processor import CSVProcessor
from pathlib import Path

@pytest.fixture
def csv_files():
    return {
        'main': Path('../data/globalterrorismdb_1000.csv'),
        'secondary': Path('../data/RAND_Database_5000.csv'),
    }

def test_main_csv_can_be_loaded(csv_files):
    """בדיקה שאפשר לטעון את הקובץ הראשי"""
    df = CSVProcessor.load_csv(csv_files['main'], num_rows=5)
    assert len(df) == 5
    assert all(col in df.columns for col in ['iyear', 'country_txt', 'city'])

def test_secondary_csv_can_be_loaded(csv_files):
    """בדיקה שאפשר לטעון את הקובץ המשני"""
    df = CSVProcessor.load_csv(csv_files['secondary'], num_rows=5)
    assert len(df) == 5
    assert all(col in df.columns for col in ['Date', 'City', 'Country'])

def test_event_creation_from_main_csv(csv_files):
    """בדיקת יצירת אירועים מהקובץ הראשי"""
    events = CSVProcessor.process_main_csv(csv_files['main'], limit=2)
    assert len(events) > 0
    event = events[0]
    assert event.title
    assert event.location
    assert event.coordinates

def test_event_creation_from_secondary_csv(csv_files):
    """בדיקת יצירת אירועים מהקובץ המשני"""
    events = CSVProcessor.process_secondary_csv(csv_files['secondary'], limit=2)
    assert len(events) > 0
    event = events[0]
    assert event.title
    assert event.location