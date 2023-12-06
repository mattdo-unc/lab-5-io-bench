#!/usr/bin/env python3

import pandas as pd
import sys

if len(sys.argv) != 3:
    print(
        "Usage: python calculate_mean.py <input_csv_file> <output_csv_file>")
    sys.exit(1)

input_csv_file = sys.argv[1]
output_csv_file = sys.argv[2]

try:
    data = pd.read_csv(input_csv_file)
except FileNotFoundError:
    print(f"File '{input_csv_file}' not found.")
    sys.exit(1)

# Strip whitespace from column names
data.columns = data.columns.str.strip()
grouped = data.groupby(
    ['Device', 'IO_Size', 'Stride', 'Operation', 'Pattern'])
mean_data = grouped[['Time (s)', 'Throughput (GB/s)']].mean().reset_index()
mean_data.to_csv(output_csv_file, index=False)

print(f"Mean data saved to '{output_csv_file}'.")
