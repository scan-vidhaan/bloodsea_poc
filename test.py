import pandas as pd
import requests

class LocateDonor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"

    def fetch_lat_long(self, pincode):
        try:
            params = {
                'postalcode': pincode,
                'country': 'India',
                'format': 'json',
            }
            headers = {'User-Agent': 'LocateDonorApp/1.0'}
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            data = response.json()
            if response.status_code == 200 and len(data) > 0:
                lat = data[0].get('lat', None)
                lon = data[0].get('lon', None)
                return lat, lon
            else:
                return None, None
        except Exception as e:
            print(f"Error fetching data for pincode {pincode}: {e}")
            return None, None

    def process_csv(self):
        try:
            df = pd.read_csv(self.input_file)
            if 'Pincode' not in df.columns:
                raise ValueError("CSV must have a 'pincode' column.")

            df['latitude'], df['longitude'] = zip(*df['Pincode'].apply(self.fetch_lat_long))
            

            df.to_csv(self.output_file, index=False)
            print(f"Processed file saved to {self.output_file}")
        except Exception as e:
            print(f"Error processing CSV: {e}")
