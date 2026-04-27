import unittest
import os
import random
import numpy as np
import pandas as pd
from numpy.random import default_rng
from badgers.generators.time_series.changepoints import RandomChangeInMeanGenerator
from badgers.generators.time_series.patterns import Pattern, add_offset, \
    add_linear_trend, scale, RandomlySpacedConstantPatterns, RandomlySpacedLinearPatterns, RandomlySpacedPatterns
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import sys

class TestChangePointGenerator(unittest.TestCase):
    
    def setUp(self):
        self.random_generator = default_rng(seed=0)
        self.n_patterns = self.args.n_patterns
        self.min_width_patterns = self.args.min_width_patterns
        self.max_width_patterns = self.args.max_width_patterns

    def test_RandomChangeInMeanGenerator_generate(self):
        # Load data from the newest CSV file
        seed = 0
        rng = default_rng(seed)
        data = pd.read_csv(self.find_newest_csv_file())
       
        # # Prepare DataFrame for the generator
        X = pd.DataFrame(data=data[self.column_name], dtype=float)
        lenth = random.randint(5, 10)
        p = Pattern(values=np.random.randn(lenth))

        generator = RandomlySpacedPatterns(random_generator=rng)
        Xt, _ = generator.generate(X.copy(), y=None, n_patterns=self.n_patterns, min_width_pattern=self.min_width_patterns
                                   , max_width_patterns=self.max_width_patterns, pattern=p)
        
        # Plot the original and generated data
        self.plot_generated_data(X[self.column_name].values, Xt)
        self.save_to_csv(X[self.column_name].values, Xt[self.column_name].values)
        
    def plot_generated_data(self, original, generated):
        plt.figure(figsize=(30, 15))

        # Plotting the original data with bold lines and larger labels
        plt.plot(original, label='Original Data', color='blue', alpha=1, linewidth=2)
        plt.plot(generated, label='Data with Patterns Generation', color='orange', alpha=1, linewidth=5)

        # Set titles and labels with larger font sizes
        plt.title('Original and Generated Data with Generated Patterns', fontsize=40)
        plt.xlabel('Index', fontsize=30)
        plt.ylabel('Value', fontsize=30)
        plt.legend(fontsize=28)
        plt.grid()
        plt.tight_layout()
        plt.show()  # Show the plot

    def save_to_csv(self, original_data, generated_data):
        # Create a timestamp for the filename
        csv_file_path = self.find_newest_csv_file().replace('roscsv', 'badger/randompatterns')
        filename = csv_file_path
        # Create a DataFrame with both original and generated data
        df = pd.DataFrame({
            'Original Data': original_data,  # Original data
            'Data with Patterns Generation': generated_data  # Generated data with change points
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
    parser.add_argument('--n_patterns', type=int, default=1, help="Number of patterns to generate")
    parser.add_argument('--min_width_patterns', type=int, default=1, help="Min_width_patterns")
    parser.add_argument('--max_width_patterns', type=int, default=1, help="Max_width_patterns")
    args, unknown = parser.parse_known_args()  # Parse known args and leave the rest for unittest

    TestChangePointGenerator.column_name = args.column
    TestChangePointGenerator.args = args
    unittest.main(argv=[sys.argv[0]] + unknown)
