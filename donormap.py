import folium
import pandas as pd
import numpy as np  # For checking NaN values

class DonorLocationPlotter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = pd.read_csv(self.input_file)

        # Normalize column names by stripping spaces and converting to lowercase
        self.df.columns = self.df.columns.str.strip().str.lower()

    def plot_locations(self):
        try:
            # Check if necessary columns exist after normalization
            required_columns = ['name of the donor', 'donor blood group', 'address', 'donor gender', 'latitude', 'longitude']
            missing_columns = [col for col in required_columns if col not in self.df.columns]

            if missing_columns:
                raise ValueError(f"CSV is missing the following columns: {', '.join(missing_columns)}")

            # Create a base map centered at a default location (e.g., Bangalore)
            base_map = folium.Map(location=[12.9716, 77.5946], zoom_start=12)  # Center on Bangalore

            # Iterate through the data and add markers
            for index, row in self.df.iterrows():
                latitude = row['latitude']
                longitude = row['longitude']

                # Skip rows where latitude or longitude are NaN
                if pd.isna(latitude) or pd.isna(longitude):
                    print(f"Skipping row {index} due to missing latitude/longitude.")
                    continue

                # Create popup with details like name, blood group, address, and gender
                popup_info = f"Name: {row['name of the donor']}<br>Blood Group: {row['donor blood group']}<br>Address: {row['address']}<br>Gender: {row['donor gender']}"

                # Add marker to the map
                folium.Marker([latitude, longitude], popup=popup_info).add_to(base_map)

            # Save the map as an HTML file
            base_map.save("donor_locations_map.html")
            print("Map saved to donor_locations_map.html")

        except Exception as e:
            print(f"Error while plotting locations: {e}")

