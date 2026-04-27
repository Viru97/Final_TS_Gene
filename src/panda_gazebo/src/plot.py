#!/usr/bin/env python3
import os
import rospy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse

class DistancePlotterNode:
    def __init__(self, joint_state_column):
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
        self.real_joint_states = self.data[f'field.real_joint_states.position{joint_state_column}']
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

        # Create the plot
        plt.figure(figsize=(30, 15))

        # Plot each joint state
        for i in range(7):
            plt.plot(self.joint_states[f'position{i}'], label=f'Virtual Joint Position {i}', alpha=0.7, linewidth=5)

        plt.plot(self.real_joint_states, label='Real Joint Position', color='black', linewidth=5)
        # Highlight areas where distance conditions are met
        for index in range(len(self.distance_hand1)):
            if combined_condition[index]:
                plt.axvspan(index - 0.5, index + 0.5, color='red', alpha=0.3)

            # Highlight areas where fault conditions are met
            if fault_condition[index]:
                plt.axvspan(index - 0.5, index + 0.5, color='yellow', alpha=0.3)

        red_patch = patches.Patch(color='red', alpha=1.0, label='Safety Violation')
        orange_patch = patches.Patch(color='orange', alpha=1.0, label='Fault Injected & Safety Violation')
        yellow_patch = patches.Patch(color='yellow', alpha=1.0, label='Fault Injected')

        # Set font sizes
        label_font_size = 30
        legend_font_size = 28

        # Add labels and title with increased font size
        plt.xlabel('Timestamps', fontsize=label_font_size)
        plt.ylabel('Joint Position (rad)', fontsize=label_font_size)
        
        # Increase font size for ticks
        plt.xticks(fontsize=label_font_size)
        plt.yticks(fontsize=label_font_size)

        # plt.legend(fontsize=legend_font_size)
        plt.legend(handles=[*plt.gca().get_legend_handles_labels()[0], red_patch, yellow_patch, orange_patch], fontsize=legend_font_size)
        plt.grid()

        # Center the plot by adjusting the layout
        plt.tight_layout()  # Adjust subplots to fit into figure area.
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust margins

        # Show the plot
        plt.show()  # Non-blocking show

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
    parser = argparse.ArgumentParser(description="Distance Plotter Node")
    parser.add_argument('--joint_state_column', type=str, required=True, help="Column name for the joint state (e.g., 'field.real_joint_states.position0')")
    
    args = parser.parse_args()

    try:
        distance_plotter_node = DistancePlotterNode(args.joint_state_column)

    except rospy.ROSInterruptException:
        pass
