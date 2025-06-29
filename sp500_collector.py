import datetime
from scraper import fetch_sp500_data, parse_sp500_data
from file_operations import save_to_csv

def collect_sp500_data(filename=None):
    """Fetch, parse, and save S&P 500 data"""
    url = "https://www.slickcharts.com/sp500"
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"sp500_prices_{timestamp}.csv"
    
    # Fetch HTML data
    html_data = fetch_sp500_data(url)
    if not html_data:
        return None

    # Parse data
    parsed_data = parse_sp500_data(html_data)
    if parsed_data is None or parsed_data.empty:
        return None

    # Save to CSV
    csv_path = save_to_csv(parsed_data, filename)
    return parsed_data, csv_path