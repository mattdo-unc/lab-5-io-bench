#!/bin/bash

# Run datagen.sh first to generate the data files
# Set up Python environment, and run Python programs
echo "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Python programs
echo "Running Python programs..."

# Generate means and confidence intervals for sda2, sdb1
python3 generate_means.py bench_sda2_cleaned.csv mean_data_sda2.csv
python3 generate_ci.py bench_sda2_cleaned.csv ci_data_sda2.csv
python3 generate_means.py bench_sdb1_cleaned.csv mean_data_sdb1.csv
python3 generate_ci.py bench_sdb1_cleaned.csv ci_data_sdb1.csv

# Generate graphs for sda2 and sdb1
python3 graph_io.py mean_data_sda2.csv ci_data_sda2.csv
python3 graph_io.py mean_data_sdb1.csv ci_data_sdb1.csv
python3 graph_io_random.py mean_data_sda2.csv ci_data_sda2.csv
python3 graph_io_random.py mean_data_sdb1.csv ci_data_sdb1.csv
python3 graph_stride.py mean_data_sda2.csv ci_data_sda2.csv
python3 graph_stride.py mean_data_sdb1.csv ci_data_sdb1.csv
python3 graph_stride_read.py mean_data_sda2.csv ci_data_sda2.csv
python3 graph_stride_read.py mean_data_sdb1.csv ci_data_sdb1.csv

# Deactivate the virtual environment
deactivate

echo "All tasks completed."
