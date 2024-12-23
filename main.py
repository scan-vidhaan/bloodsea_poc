# Try importing the LocateDonor class from the test module
try:
    from test import LocateDonor 
    from donormap import DonorLocationPlotter
    from intentanalyzer import BloodDonationIntentAnalyzer
    from behaviouranalysis import DonorAnalyzer
    from donor_server import CSVToPostgres
     # Assuming 'test.py' contains LocateDonor class
    print("Import Successful")
except ImportError as e:
    print(f"Import Failed: {e}")
    
    
def behaviour_analysis():
        donor_analyzer = DonorAnalyzer('input.csv')
        donor_analyzer.load_data()
        donor_analyzer.calculate_behavior_scores()
        donor_analyzer.save_results('input.csv')


def donor_location():
        geocode = LocateDonor("input.csv", "input.csv")  # Overwriting the input file
        geocode.process_csv()
        donorMap=DonorLocationPlotter("input.csv")
        donorMap.plot_locations()

def send_data_to_server():
      DATABASE_URL = "postgresql://admin:JAc6pXCdY0vMQzOHGKonb2O3zpdNXd4R@dpg-ct95fdl6l47c73an6bpg-a.oregon-postgres.render.com/donordb"
      CSV_FILE_PATH = "data.csv"
      TABLE_NAME = "my_table"
      csv_to_postgres = CSVToPostgres(DATABASE_URL, CSV_FILE_PATH, TABLE_NAME)
      try:
        csv_to_postgres.connect_to_database()
        csv_to_postgres.insert_csv_data()
      except Exception as e:
        print(f"An error occurred: {e}")
      finally:
        csv_to_postgres.close_connection()

            
     
   
def intent_analysis():
 
         analyzer = BloodDonationIntentAnalyzer()
    
    # Step 1: Load intents from a CSV file
         analyzer.load_csv("input.csv")
    
    # Step 2: Initialize relevant terms for blood donation context
         analyzer.initialize_keywords()
    
    # Step 3: Populate arrays dynamically from the data
         analyzer.populate_arrays_from_data()
    
    # Step 4: Process intents and calculate scores
         analyzer.process_intents()
    
    # Step 5: Save scored intents to the same CSV file (overwrite)
         analyzer.save_csv("input.csv")

# Main logic to process the CSV file
def main():
 donor_location()
 intent_analysis()
 behaviour_analysis()
 send_data_to_server()
   





# Run the main function
if __name__ == "__main__":
    main()
 
