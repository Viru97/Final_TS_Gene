import unittest
import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from badgers.generators.time_series.missingness import MissingAtRandomGenerator
from datetime import datetime
import sys  # Add sys for argument handling

class TestMissingAtRandomGenerator(unittest.TestCase):

    def setUp(self) -> None:
        # Load data from the CSV file
        self.data = pd.read_csv(self.find_newest_csv_file())

        # Ensure the correct column is selected for generating missingness
        if self.column_name not in self.data.columns:
            raise ValueError(f"CSV does not contain the '{self.column_name}' column.")
        
        # Prepare data for the generator
        self.X = self.data[self.column_name].values.reshape(-1, 1)

    def test_generator(self):
        # Use the passed n_missing parameter from the command line
        n_missing = self.n_missing
        generator = MissingAtRandomGenerator()

        # Generate data with missing values
        Xt, _ = generator.generate(self.X.copy(), y=None, n_missing=n_missing)
        # Plot the original and modified data
        self.plot_data(self.X, Xt.values.flatten())
        self.save_to_csv(self.X, Xt.values.flatten())

    def plot_data(self, original, generated):
        plt.figure(figsize=(30, 15))
        
        # Plot original data
        plt.plot(original, label='Original Data', color='blue', alpha=1, linewidth=2)

        # Plot data with missingness
        plt.plot(generated, label='Data with Missing Values', color='orange', alpha=1, linewidth=5)

        # Set titles and labels
        plt.title('Original and Data with Missing Values', fontsize=40)
        plt.xlabel('Index', fontsize=30)
        plt.ylabel('Value', fontsize=30)
        plt.legend(fontsize=28)
        plt.grid()
        plt.tight_layout()

        # Show the plot
        plt.show()

    def save_to_csv(self, original_data, generated_data):
        # Create a timestamp for the filename
        csv_file_path = self.find_newest_csv_file().replace('roscsv', 'badger/missingpoints')
        filename = csv_file_path
        
        # Create a DataFrame with both original and generated data
        df = pd.DataFrame({
            'Original_Data': original_data.flatten(),  # Flatten to convert to 1D array
            'Data_With_Missing_Values': generated_data.flatten()  # Flatten to convert to 1D array
        })
        
        # Save to CSV
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def find_newest_csv_file(self):
        self.csv_directory = '/home/baua/Final_TS_Gene/data/roscsv/'
        csv_files = [f for f in os.listdir(self.csv_directory) if f.endswith('.csv')]
        if not csv_files:
            raise FileNotFoundError("No csv files found in the directory.")

        # Sort the files by modification time (newest first)
        csv_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.csv_directory, f)), reverse=True)
        
        # Return the path to the newest csv file
        newest_csv_file = os.path.join(self.csv_directory, csv_files[0])
        return newest_csv_file

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Test MissingAtRandomGenerator with custom CSV column and n_missing")
    parser.add_argument('--column', type=str, required=True, help="Column name for data in the CSV file")
    parser.add_argument('--n_missing', type=int, required=True, help="Number of missing values to generate")
    args, unknown = parser.parse_known_args()  # Parse known args, let unittest handle the rest

    # Set the column name and n_missing for the test
    TestMissingAtRandomGenerator.column_name = args.column
    TestMissingAtRandomGenerator.n_missing = args.n_missing

    # Run the unittest, ignore extra args for unittest
    unittest.main(argv=[sys.argv[0]] + unknown)
