import requests
import csv
from textblob import TextBlob
import json
import re 

class BloodDonationIntentAnalyzer:
    def __init__(self, array_file="arrays.json"):
        """
        Initialize the intent analyzer with empty arrays for social service
        and health benefits terms, and an optional file to save/load arrays.
        """
        self.social_service_terms = set()
        self.health_benefit_terms = set()
        self.records = []
        self.array_file = array_file

    def fetch_related_words(self, query):
        """
        Fetch related words from the Datamuse API for the given query.
        Args:
            query (str): The context or phrase to fetch related words for.
        Returns:
            set: A set of related words.
        """
        url = f"https://api.datamuse.com/words?ml={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return {item['word'] for item in response.json()}
        return set()

    def initialize_keywords(self):
        """
        Initialize keywords dynamically using the API for blood donation context.
        """
        if not self.social_service_terms:
            # Fetch terms related to altruistic blood donation
            self.social_service_terms = self.fetch_related_words("helping society") | \
                                        self.fetch_related_words("life-saving donations") | self.fetch_related_words("save")|self.fetch_related_words("help")
        if not self.health_benefit_terms:
            # Fetch terms related to health benefits of blood donation
            self.health_benefit_terms = self.fetch_related_words("benefits of blood donation") | \
                                        self.fetch_related_words("health advantages of donating blood") |  self.fetch_related_words("rbcs") | self.fetch_related_words("health")

    def load_csv(self, file_path):
        """
        Load intent data from a CSV file into records.
        Args:
            file_path (str): Path to the CSV file.
        """
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            self.records = [{"Intent": row["Intent"], "Impact Score": 0} for row in reader]

    def populate_arrays_from_data(self):
        """
        Analyze intent data, extract impactful words dynamically, and expand arrays.
        """
        self.initialize_keywords()  # Ensure keywords are initialized

        word_context = {}
        for record in self.records:
            intent = record["Intent"].lower()
            words = set(intent.split())
            for word in words:
                if word not in word_context:
                    word_context[word] = []
                word_context[word].append(intent)

        # Expand terms based on context and sentiment
        for word, contexts in word_context.items():
            social_score = 0
            health_score = 0
            for context in contexts:
                sentiment = TextBlob(context).sentiment.polarity
                if sentiment > 0:  # Consider only positive contexts
                    print("sentiment is positive")
                    if word in self.social_service_terms:
                        social_score += 1
                    if word in self.health_benefit_terms:
                        health_score += 1

            # Add highly relevant words to arrays
            if social_score > health_score:
                self.social_service_terms.add(word)
            elif health_score > social_score:
                self.health_benefit_terms.add(word)

        self.save_arrays()

    def save_arrays(self):
     pass

    def process_intents(self):
        """
        Calculate impact scores for each intent using the populated arrays.
        """
        for record in self.records:
            intent = record["Intent"]
            score = 0
            
            # Check for social service-related terms
            for word in self.social_service_terms:
                if word in intent.lower():
                    score += 3  # Higher weight for social service terms
            
            # Check for health benefit-related terms
            for word in self.health_benefit_terms:
                if word in intent.lower():
                    score += 2  # Lower weight for health benefits terms
            
            # Check for 'activity points' term and give it a score of 1
            if 'activity points' in intent.lower():
                score = 0  # Give 1 point for activity points
            
            # Assign score to the record
            record["Impact Score"] = score

    def save_csv(self, file_path):
        """
        Save the scored intents to the same CSV file, appending the Impact Score column.
        Args:
            file_path (str): Path to save the CSV file.
        """
        # Open the input CSV file for reading and writing
        with open(file_path, 'r+', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            # Rewind the file and write back the header with the new 'Impact Score' column
            file.seek(0)
            fieldnames = reader.fieldnames + ["Impact Score"]  # Add Impact Score to header
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            # Append the 'Impact Score' to each row and write it back to the file
            for i, row in enumerate(rows):
                row["Impact Score"] = self.records[i]["Impact Score"]  # Append Impact Score to the row
                writer.writerow(row)


   
