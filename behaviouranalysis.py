import pandas as pd

class DonorAnalyzer:
    def __init__(self, file_path):
        """Initialize with CSV file path."""
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Load the dataset from the CSV file."""
        self.data = pd.read_csv(self.file_path)
        print("Data loaded successfully.")

    def clean_value(self, value):
        """Clean up the column values by stripping spaces and converting to lowercase."""
        if isinstance(value, str):
            return value.strip().lower()
        return value

    def assign_weights(self, row, max_intent_score):
        """Calculate Behavior Analysis score for a single donor."""
        try:
            score = 0
            
            # Assign weights based on conditions with cleaned values
            score += 0.9 if self.clean_value(row['Have you donated platelets']) == 'Yes' else 0.6
            score += 0 if not str(row['Number of donations']).isdigit() else \
                (0.2 if int(row['Number of donations']) == 0 else \
                 0.5 if int(row['Number of donations']) <= 2 else 0.8)
            score += 1 if self.clean_value(row['Are you under any medical condition']) == 'No' else 0
            score += 1 if self.clean_value(row['Will you donate blood if you stay close to needy.']) == 'Yes' else 0.5
            score += 1 if self.clean_value(row['Do you Smoke']) == 'No' else 0.3
            score += 1 if self.clean_value(row['Do you Drink']) == 'I do not drink' else \
                     0.7 if self.clean_value(row['Do you Drink']) == 'Ocationally' else 0.3
            score += 1.5 if self.clean_value(row['Will you donate blood during an emergency ?']) == 'Yes' else 0.5
            score += 1 if self.clean_value(row['blood donation drive']) == 'Yes' else 0.5
            score += 1 if self.clean_value(row['Comfort']) == 'Very Comfortable' else \
                     0.8 if self.clean_value(row['Comfort']) == 'Comfortable' else \
                     0.6 if self.clean_value(row['Comfort']) == 'Nutral' else 0.3
            score += 1 if self.clean_value(row['actvity_points']) == 'no' else 0.3
            score += 1.5 if self.clean_value(row['Have you donated blood during an emergency ?']) == 'YES' else 1
            
            # Normalize Impact Score using the max value from the column
            score += (row['Impact Score'] / max_intent_score) * 0.8  # Use dynamic max value
            return score
        except KeyError as e:
            print(f"Missing column in data: {e}")
            return 0

    def calculate_behavior_scores(self):
        """Add the Behavior Analysis column to the dataset."""
        if self.data is not None:
            max_intent_score = self.data['Impact Score'].max()  # Get the max Impact Score from the dataset
            self.data['Behavior Analysis'] = self.data.apply(lambda row: self.assign_weights(row, max_intent_score), axis=1)
            print("Behavior Analysis scores calculated.")
        else:
            print("No data loaded.")

    def save_results(self, output_file):
        """Save the dataset with scores to a new CSV file."""
        if self.data is not None:
            self.data.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}.")
        else:
            print("No data to save.")

