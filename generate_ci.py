#!/usr/bin/env python3

import pandas as pd
import sys
import numpy as np
import scipy.stats as stats

# Check if a CSV file name is provided as a command-line argument
if len(sys.argv) != 3:
    print(
        "Usage: python calculate_mean_and_ci.py <input_csv_file> <output_csv_file>")
    sys.exit(1)

input_csv_file = sys.argv[1]
output_csv_file = sys.argv[2]

try:
    data = pd.read_csv(input_csv_file)
except FileNotFoundError:
    print(f"File '{input_csv_file}' not found.")
    sys.exit(1)

data.columns = data.columns.str.strip()
grouped = data.groupby(
    ['Device', 'IO_Size', 'Stride', 'Operation', 'Pattern'])

# Calculate the mean and confidence interval for Time (s)
# and Throughput (GB/s) for each group
mean_data = grouped[['Time (s)', 'Throughput (GB/s)']].mean().reset_index()
confidence_intervals = grouped[['Time (s)', 'Throughput (GB/s)']].agg(
    lambda x: stats.t.interval(0.95, len(x) - 1, loc=np.mean(x),
                               scale=stats.sem(x))
).reset_index(drop=True)

# Combine the mean and confidence interval data
mean_data['Time (s) - Lower CI'] = confidence_intervals['Time (s)'].apply(
    lambda x: x[0])
mean_data['Time (s) - Upper CI'] = confidence_intervals['Time (s)'].apply(
    lambda x: x[1])
mean_data['Throughput (GB/s) - Lower CI'] = confidence_intervals[
    'Throughput (GB/s)'].apply(lambda x: x[0])
mean_data['Throughput (GB/s) - Upper CI'] = confidence_intervals[
    'Throughput (GB/s)'].apply(lambda x: x[1])

# Save the mean and confidence interval data to a new CSV file
mean_data.to_csv(output_csv_file, index=False)
print(f"Mean and confidence interval data saved to '{output_csv_file}'.")
