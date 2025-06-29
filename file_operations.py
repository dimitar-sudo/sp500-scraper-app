import os
import re

def save_to_csv(data, filename):
    """Save DataFrame to CSV in 'data' directory."""
    try:
        # Create absolute path to data directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Sanitize filename
        clean_name = re.sub(r'[\\/*?:"<>|]', "", filename)
        if not clean_name.lower().endswith('.csv'):
            clean_name += '.csv'
            
        # Create full path
        path = os.path.join(data_dir, clean_name)
        data.to_csv(path, index=False)
        return path
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return None