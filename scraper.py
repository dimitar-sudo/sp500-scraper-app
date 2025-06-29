import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def fetch_sp500_data(url):
    """Fetch S&P 500 data from URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        if 'text/html' not in response.headers.get('Content-Type', ''):
            print(f"Unexpected content type: {response.headers.get('Content-Type')}")
            return None
            
        return response.text
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_sp500_data(html_data):
    """Parse HTML to extract stock data table."""
    try:
        soup = BeautifulSoup(html_data, 'html.parser')
        table = soup.select_one('table.table.table-hover.table-borderless.table-sm')
        
        if table is None:
            print("Could not find the S&P 500 table with the expected classes.")
            return None
            
        table_html = str(table)
        df = pd.read_html(StringIO(table_html))[0]
        
        for col in ['Weight', 'Price', 'Chg', '% Chg']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: x.strip('()') if isinstance(x, str) else x)
        
        df.columns = [col.strip() for col in df.columns]
        
        return df[['Company', 'Symbol', 'Weight', 'Price', 'Chg', '% Chg']]
    except Exception as e:
        print(f"Error parsing HTML data: {e}")
        return None