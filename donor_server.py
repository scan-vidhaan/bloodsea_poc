import csv
import psycopg2

class CSVToPostgres:
    def __init__(self, database_url, csv_file_path, table_name):
        self.database_url = database_url
        self.csv_file_path = csv_file_path
        self.table_name = table_name
        self.connection = None
        self.cursor = None

    def connect_to_database(self):
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

    def table_exists(self):
        try:
            self.cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{self.table_name}');")
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Error checking if table exists: {e}")
            raise

    def sanitize_column_names(self, columns):
        return [col.replace(' ', '_') for col in columns]

    def create_table_based_on_csv_header(self, csv_header):
        try:
            sanitized_columns = self.sanitize_column_names(csv_header)
            columns = [f"{col} VARCHAR(255)" for col in sanitized_columns]
            create_table_query = f"CREATE TABLE {self.table_name} (id SERIAL PRIMARY KEY, {', '.join(columns)});"
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{self.table_name}' created based on CSV header.")
        except Exception as e:
            print(f"Error creating table: {e}")
            raise

    def delete_existing_data(self):
        try:
            self.cursor.execute(f"DELETE FROM {self.table_name};")
            self.connection.commit()
            print(f"All existing data in '{self.table_name}' deleted.")
        except Exception as e:
            print(f"Error deleting existing data: {e}")
            raise

    def insert_csv_data(self):
        try:
            with open(self.csv_file_path, "r") as file:
                csv_reader = csv.reader(file)
                csv_header = next(csv_reader)  # Read header row
                sanitized_header = self.sanitize_column_names(csv_header)

                if self.table_exists():
                    print(f"Table '{self.table_name}' exists.")
                    self.delete_existing_data()
                else:
                    print(f"Table '{self.table_name}' does not exist. Creating table.")
                    self.create_table_based_on_csv_header(csv_header)

                for row in csv_reader:
                    placeholders = ', '.join(['%s'] * len(row))
                    self.cursor.execute(f"INSERT INTO {self.table_name} ({', '.join(sanitized_header)}) VALUES ({placeholders});", row)

                self.connection.commit()
                print("CSV data inserted into the table successfully.")
        except Exception as e:
            print(f"Error inserting CSV data: {e}")
            raise

if __name__ == "__main__":
    DATABASE_URL = "postgresql://admin:JAc6pXCdY0vMQzOHGKonb2O3zpdNXd4R@dpg-ct95fdl6l47c73an6bpg-a.oregon-postgres.render.com/donordb"
    CSV_FILE_PATH = "input.csv"
    TABLE_NAME = "donor_datadump"

    csv_to_postgres = CSVToPostgres(DATABASE_URL, CSV_FILE_PATH, TABLE_NAME)

    try:
        csv_to_postgres.connect_to_database()
        csv_to_postgres.insert_csv_data()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        csv_to_postgres.close_connection()
