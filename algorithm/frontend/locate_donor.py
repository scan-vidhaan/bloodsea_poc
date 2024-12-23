import pandas as pd
import requests
import geopy.distance
import csv
import os

class LocationService:
    def __init__(self, pincode, blood_group):
        self.pincode = pincode
        self.blood_group = blood_group

        # Adjust the path to input.csv and output.csv
        self.input_file = "input.csv"
        self.output_file = "output.csv"

        self.donors_data = []  # List to store final data
        self.pincode_lat = None
        self.pincode_lon = None

    def get_lat_lon(self):
        """Fetch latitude and longitude from the given pincode using OpenStreetMap."""
        url = f"https://nominatim.openstreetmap.org/search?postalcode={self.pincode}&country=India&format=json"
        headers = {
            "User-Agent": "BloodSeaApp/1.0 (contact@yourdomain.com)"  # Replace with your app's details
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            json_response = response.json()
            if json_response:
                self.pincode_lat = float(json_response[0]['lat'])
                self.pincode_lon = float(json_response[0]['lon'])
                print(f"Coordinates for pincode {self.pincode}: {self.pincode_lat}, {self.pincode_lon}")
            else:
                raise ValueError("No results found for the given pincode.")
        elif response.status_code == 403:
            raise ValueError("Access denied by the API. Check the User-Agent header.")
        else:
            raise ValueError(f"Failed to fetch coordinates: {response.status_code}")

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two lat/long points in kilometers."""
        if None in [lat1, lon1, lat2, lon2]:
            raise ValueError("Coordinates must not be None.")
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)
        return geopy.distance.distance(coords_1, coords_2).km

    def read_csv(self):
        """Read the input CSV file."""
        try:
            return pd.read_csv(self.input_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.input_file} not found. Ensure the file exists.")

    def write_to_output_csv(self, output_data):
        """Write the filtered data to the output CSV."""
        headers = ["Name of the donor", "Donor mobile number", "address", "Behavior Analysis", "Distance (km)"]

        # Write only headers if output_data is empty
        if not output_data:
            print("No matching donors found. Writing only headers to the output CSV.")
            with open(self.output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
            return

        # Write full data if output_data is not empty
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(output_data)

    def process_data(self):
        """Process the input CSV, filter by blood group, calculate distance, and sort by distance."""
        input_data = self.read_csv()
        output_data = []

        # Fetch latitude and longitude for the pincode
        self.get_lat_lon()

        for index, row in input_data.iterrows():
            if row['Donor Blood group'] == self.blood_group:
                donor_lat = row.get('latitude')
                donor_lon = row.get('longitude')

                # Skip donors with missing coordinates
                if pd.isna(donor_lat) or pd.isna(donor_lon):
                    print(f"Skipping donor at index {index} due to missing coordinates.")
                    continue

                try:
                    # Calculate the distance
                    distance = self.calculate_distance(self.pincode_lat, self.pincode_lon, donor_lat, donor_lon)
                    print("distance is")
                    print(distance)
                    row['Distance (km)'] = distance
                except ValueError as e:
                    print(f"Skipping donor at index {index}: {e}")
                    continue

                # Filter donors with Behavior Analysis score > 4.8
                if row['Behavior Analysis'] > 4.8:
                    output_data.append({
                        "Name of the donor": row['Name of the donor'],
                        "Donor mobile number": row['Donor mobile number'],
                        "address": row['address'],
                        "Behavior Analysis": row['Behavior Analysis'],
                        "Distance (km)": distance
                    })

        # Sort by distance and select top 5 closest
        output_data.sort(key=lambda x: x['Distance (km)'])
        output_data = output_data[:5]
        print("output values")
        print(output_data)

        # Write the filtered data to output.csv
        self.write_to_output_csv(output_data)

        # Prepare data for Streamlit display
        self.donors_data = [
            {
                "Name": row["Name of the donor"],
                "Mobile": row["Donor mobile number"],
                "Address": row["address"],
                "Score": row["Behavior Analysis"],
                "Distance": row["Distance (km)"]
            } for row in output_data
        ]
        return self.donors_data
