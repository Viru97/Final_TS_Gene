import unittest
import os
import numpy as np
import pandas as pd
from numpy.random import default_rng
from badgers.generators.time_series.trends import GlobalAdditiveLinearTrendGenerator, AdditiveLinearTrendGenerator
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import sys

class TestChangePointGenerator(unittest.TestCase):
    
    def setUp(self):
        self.random_generator = default_rng(seed=0)
        # Set the values dynamically from the command-line arguments
        # self.n_changepoints = self.args.n_changepoints
        # self.min_change = self.args.min_change
        # self.max_change = self.args.max_change

    def test_RandomChangeInMeanGenerator_generate(self):
        # Load data from the newest CSV file
        seed = 0
        rng = default_rng(seed)
        data = pd.read_csv(self.find_newest_csv_file())

        # # Ensure the correct column is selected for generating change points
        # if self.column_name not in X.columns:
        #     raise ValueError(f"CSV does not contain the '{self.column_name}' column.")
        
        # # Prepare DataFrame for the generator
        X = pd.DataFrame(data=data[self.column_name], dtype=float)
        generator = AdditiveLinearTrendGenerator(random_generator=rng)
        Xt, _ = generator.generate(X, y=None, slope=np.array([0.1]))
        
        # Plot the original and generated data
        self.plot_generated_data(X[self.column_name].values, Xt)
        self.save_to_csv(X[self.column_name].values, Xt[self.column_name].values)
        
    def plot_generated_data(self, original, generated):
        plt.figure(figsize=(30, 15))

        # Plotting the original data with bold lines and larger labels
        plt.plot(original, label='Original Data', color='blue', alpha=1, linewidth=2)
        plt.plot(generated, label='Data with Trends Generation', color='orange', alpha=1, linewidth=5)

        # Set titles and labels with larger font sizes
        plt.title('Original and Generated Data with Generated Trends', fontsize=40)
        plt.xlabel('Index', fontsize=30)
        plt.ylabel('Value', fontsize=30)
        plt.legend(fontsize=28)
        plt.grid()
        plt.tight_layout()
        plt.show()  # Show the plot

    def save_to_csv(self, original_data, generated_data):
        # Create a timestamp for the filename
        csv_file_path = self.find_newest_csv_file().replace('roscsv', 'badger/changingpoints')
        filename = csv_file_path
        # Create a DataFrame with both original and generated data
        df = pd.DataFrame({
            'Original_Data': original_data,  # Original data
            'Data_With_Changing_Values': generated_data  # Generated data with change points
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
    # parser.add_argument('--column', type=str, required=True, help="Column name for data in the CSV file")
    # parser.add_argument('--n_changepoints', type=int, default=1, help="Number of change points to generate")
    # parser.add_argument('--min_change', type=float, default=-1, help="Minimum change value for change points")
    # parser.add_argument('--max_change', type=float, default=1, help="Maximum change value for change points")
    args, unknown = parser.parse_known_args()  # Parse known args and leave the rest for unittest

    # Set the column name and additional parameters for the test
    # TestChangePointGenerator.column_name = args.column
    TestChangePointGenerator.column_name = 'field.real_joint_states.position1'
    TestChangePointGenerator.args = args

    # Run the unittest, ignoring additional command-line arguments meant for unittest
    unittest.main(argv=[sys.argv[0]] + unknown)
