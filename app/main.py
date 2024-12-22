from flask import Flask

from app.routes.search_routes import search_routes
from app.service.csv_processor import CSVProcessor
from app.service.elastic_service import save_events_for_terror
from app.service.fetch_service import process_news
from app.service.init_elastic import create_index

app = Flask(__name__)
app.register_blueprint(search_routes)

def import_historic_data(main_csv_path: str, secondary_csv_path: str) -> None:
    """Import historic data from both CSV files"""

    # Process main CSV
    print("Processing main CSV file...")
    main_events = CSVProcessor.process_main_csv(main_csv_path)
    save_events_for_terror(main_events)
    print(f"Saved {len(main_events)} events from main CSV")

    # Process secondary CSV
    print("Processing secondary CSV file...")
    secondary_events = CSVProcessor.process_secondary_csv(secondary_csv_path)
    save_events_for_terror(secondary_events)
    print(f"Saved {len(secondary_events)} events from secondary CSV")

if __name__ == '__main__':
    # create_index()
    # process_news()
    app.run(debug=True)

    # import_historic_data(
    #     main_csv_path='./data/globalterrorismdb_1000.csv',
    #     secondary_csv_path='./data/RAND_Database_5000.csv'
    # )
# חיפוש בסיסי בכל המקורות
# GET http://localhost:5000/search/keywords?query=bombing&limit=10
#
# # חיפוש בחדשות בזמן אמת
# GET http://localhost:5000/search/news?query=terror attack&limit=5
#
# # חיפוש במידע היסטורי
# GET http://localhost:5000/search/historic?query=assassination&limit=15
#
# # חיפוש משולב עם תאריכים
# GET http://localhost:5000/search/combined?query=explosion&start_date=2020-01-01&end_date=2024-12-31&limit=20
