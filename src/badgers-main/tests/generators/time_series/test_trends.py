import unittest
import os
import numpy as np
import pandas as pd
from numpy.random import default_rng

import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import sys

from badgers.generators.time_series.trends import AdditiveLinearTrendGenerator, \
    RandomlySpacedLinearTrends

class TestChangePointGenerator(unittest.TestCase):
    
    def setUp(self):
        self.random_generator = default_rng(seed=0)
        # Set the values dynamically from the command-line arguments
        self.slope = self.args.slope
        self.start_point = self.args.start_point

    def test_RandomChangeInMeanGenerator_generate(self):
        # Load data from the newest CSV file
        X = pd.read_csv(self.find_newest_csv_file())

        # Ensure the correct column is selected for generating change points
        if self.column_name not in X.columns:
            raise ValueError(f"CSV does not contain the '{self.column_name}' column.")
        
        # Prepare DataFrame for the generator
        X = pd.DataFrame(data=X[self.column_name], dtype=float)
        self.end_point = len(X)
        y = None
        # Generate data with change points
        generator = AdditiveLinearTrendGenerator(random_generator=self.random_generator)
        Xt, _ = generator.generate(X, y=None, slope=np.array([self.slope]), start=self.start_point, end=self.end_point)
        
        # Plot the original and generated data
        self.plot_generated_data(X[self.column_name].values, Xt)
        self.save_to_csv(X[self.column_name].values, Xt[self.column_name].values)
        
    def plot_generated_data(self, original, generated):
        plt.figure(figsize=(30, 15))

        # Plotting the original data with bold lines and larger labels
        plt.plot(original, label='Original Data', color='blue', alpha=1, linewidth=2)
        plt.plot(generated, label='Drifted Data', color='orange', alpha=1, linewidth=5)

        # Set titles and labels with larger font sizes
        plt.title('Original and Drifted Data', fontsize=40)
        plt.xlabel('Index', fontsize=30)
        plt.ylabel('Value', fontsize=30)
        plt.legend(fontsize=28)
        plt.grid()
        plt.tight_layout()
        plt.show()  # Show the plot

    def save_to_csv(self, original_data, generated_data):
        # Create a timestamp for the filename
        csv_file_path = self.find_newest_csv_file().replace('roscsv', 'badger/drifts')
        filename = csv_file_path
        # Create a DataFrame with both original and generated data
        df = pd.DataFrame({
            'Original_Data': original_data,  # Original data
            'Drifted_Data': generated_data  # Generated data with change points
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
    # Parse command line arguments for the column name and other parameters
    parser = argparse.ArgumentParser(description="Test ChangePointGenerator with custom CSV column and parameters")
    parser.add_argument('--column', type=str, required=True, help="Column name for data in the CSV file")
    parser.add_argument('--slope', type=float, default=1, help="Number of change points to generate")
    parser.add_argument('--start_point', type=int, default=-1, help="Minimum change value for change points")
    args, unknown = parser.parse_known_args()  # Parse known args and leave the rest for unittest

    # Set the column name and additional parameters for the test
    TestChangePointGenerator.column_name = args.column
    TestChangePointGenerator.args = args

    # Run the unittest, ignoring additional command-line arguments meant for unittest
    unittest.main(argv=[sys.argv[0]] + unknown)
