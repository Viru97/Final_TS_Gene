#!/usr/bin/env python3
import os
import rospy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse

class DistancePlotterNode:
    def __init__(self):
        rospy.init_node('distance_plotter_node', anonymous=True)

        # Specify your CSV file path
        csv_file_path = self.find_newest_csv_file()  # Adjust the path as needed

        # Load the CSV file
        self.data = pd.read_csv(csv_file_path)

        # Extract distance data
        self.distance_hand1 = self.data['field.distance_monitoring_hand1.data']  # Adjust the column name if necessary
        self.distance_hand2 = self.data['field.distance_monitoring_hand2.data']  # Adjust the column name if necessary

        # Extract joint states
        self.joint_states = {
            f'position{i}': self.data[f'field.virtual_joint_states.position{i}'] for i in range(7)
        }
        # Extract all real joint states
        self.all_real_joint_states = {
            f'position{i}': self.data[f'field.real_joint_states.position{i}'] for i in range(7)
        }
        # Extract fault flag data
        self.fault_flag = self.data['field.fault_flag.data']  # Adjust the column name if necessary
        # Plot the data
        self.plot_data()

    def plot_data(self):
        # Create a boolean mask for the distance conditions
        condition_hand1 = self.distance_hand1 < 0.2
        condition_hand2 = self.distance_hand2 < 0.2
        combined_condition = condition_hand1 | condition_hand2  # Highlight if either condition is met
        
        # Create a boolean mask for the fault flag condition
        fault_condition = self.fault_flag == 1  # Highlight if fault flag is set

        # Create the figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(30, 15), sharex=True)
        
        # Plot virtual and single real joint state on the first subplot
        for i in range(7):
            ax1.plot(self.joint_states[f'position{i}'], label=f'Virtual Joint Position {i}', linewidth=5)
        

        # Highlight areas where distance conditions are met
        for index in range(len(self.distance_hand1)):
            if combined_condition[index]:
                ax1.axvspan(index - 0.5, index + 0.5, color='red', alpha=0.3)

            if fault_condition[index]:
                ax1.axvspan(index - 0.5, index + 0.5, color='yellow', alpha=0.3)

        # Legend and labels for the first subplot
        ax1.set_ylabel('Virtual Joint Position (rad)', fontsize=30)
        ax1.legend(fontsize=20)

        # Plot all real joint states on the second subplot
        for i in range(7):
            ax2.plot(self.all_real_joint_states[f'position{i}'], label=f'Real Joint Position {i}', linewidth=5)
        
        ax2.set_xlabel('Timestamps', fontsize=30)
        ax2.set_ylabel('Real Joint Positions (rad)', fontsize=30)
        ax2.legend(fontsize=20)

        # Add a grid to both plots
        ax1.grid()
        ax2.grid()

        # Highlight patches for legend
        red_patch = patches.Patch(color='red', alpha=1.0, label='Safety Violation')
        orange_patch = patches.Patch(color='orange', alpha=1.0, label='Fault Injected & Safety Violation')
        yellow_patch = patches.Patch(color='yellow', alpha=1.0, label='Fault Injected')
        ax1.legend(handles=[*ax1.get_legend_handles_labels()[0], red_patch, yellow_patch, orange_patch], fontsize=20)
        ax2.legend(handles=[*ax2.get_legend_handles_labels()[0]], fontsize=20)
        # Set tick font sizes for both plots
        ax1.tick_params(axis='both', which='major', labelsize=20)
        ax2.tick_params(axis='both', which='major', labelsize=20)

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        # Show the plot
        plt.show()

        # Check if the plot window is closed
        plt.get_current_fig_manager().window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        rospy.signal_shutdown("Plot window closed")
        plt.close('all')  # Close all matplotlib plots

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

    try:
        distance_plotter_node = DistancePlotterNode()

    except rospy.ROSInterruptException:
        pass
