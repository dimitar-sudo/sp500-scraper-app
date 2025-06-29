from flask import Flask, render_template, request, session, send_file
from sp500_collector import collect_sp500_data
import uuid
import os
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = '3fa85f64f751cc20e3d026c7c4d8d3a4e1c6b924a5a3e8b7f6a5d4c3b2a1f0e9d'
app.logger.setLevel(logging.DEBUG)

# Global variable to track last update time
last_data_refresh = None
last_data_hash = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global last_data_refresh, last_data_hash
    
    error = None
    table_html = None
    download_available = False
    data_freshness = None
    
    if request.method == 'POST' and 'scrape' in request.form:
        try:
            # Generate unique filename
            filename = f"sp500_{uuid.uuid4().hex}.csv"
            
            # Collect data
            result = collect_sp500_data(filename)
            
            if result is None:
                error = "Failed to scrape data. Please try again later."
                app.logger.error("Scraping returned None")
            else:
                data, filepath = result
                
                # Check if data has changed since last scrape
                current_hash = hash(tuple(data.values.tobytes()))
                
                if last_data_hash == current_hash:
                    data_freshness = "Data has not changed since last scrape"
                else:
                    data_freshness = "New data obtained"
                    last_data_hash = current_hash
                
                # Store ABSOLUTE path in session
                session['csv_path'] = os.path.abspath(filepath)
                
                # Create HTML table
                table_html = data.to_html(
                    classes='table table-striped table-bordered table-hover',
                    index=False
                )
                download_available = True
                
                # Update last refresh time
                last_data_refresh = datetime.now()
                
        except Exception as e:
            error = f"Scraping failed: {str(e)}"
            app.logger.exception("Scraping error")
    
    return render_template(
        'index.html',
        table_html=table_html,
        error=error,
        download_available=download_available,
        last_refresh=last_data_refresh,
        data_freshness=data_freshness
    )

@app.route('/download')
def download():
    if 'csv_path' in session:
        filepath = session['csv_path']
        
        if os.path.exists(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name='sp500_data.csv',
                mimetype='text/csv'
            )
    
    return "No data available to download", 404

if __name__ == '__main__':
    app.run(debug=True)