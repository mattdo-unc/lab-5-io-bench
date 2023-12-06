#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt

# Load the stride data and confidence interval data
if len(sys.argv) != 3:
    print("Usage: python graph_stride.py <stride_data_csv_file> "
          "<ci_data_csv_file>")
    sys.exit(1)
mean_data = pd.read_csv(sys.argv[1])
ci_data = pd.read_csv(sys.argv[2])

# Filter data for random reads and writes with a Stride of 4096
random_read_mean = mean_data[(mean_data['Pattern'] == 'random') &
                             (mean_data['Operation'] == 'read') & (
                                         mean_data['Stride'] == 0)]
random_read_ci = ci_data[(ci_data['Pattern'] == 'random') &
                         (ci_data['Operation'] == 'read') & (
                                     ci_data['Stride'] == 0)]

random_write_mean = mean_data[(mean_data['Pattern'] == 'random') &
                              (mean_data['Operation'] == 'write') & (
                                          mean_data['Stride'] == 0)]
random_write_ci = ci_data[(ci_data['Pattern'] == 'random') &
                          (ci_data['Operation'] == 'write') & (
                                      ci_data['Stride'] == 0)]

# Calculate error bars
random_read_lower_err = random_read_mean['Throughput (GB/s)'] - \
                        random_read_ci['Throughput (GB/s) - Lower CI']
random_read_upper_err = random_read_ci['Throughput (GB/s) - Upper CI'] - \
                        random_read_mean['Throughput (GB/s)']

random_write_lower_err = random_write_mean['Throughput (GB/s)'] - \
                         random_write_ci['Throughput (GB/s) - Lower CI']
random_write_upper_err = random_write_ci['Throughput (GB/s) - Upper CI'] - \
                         random_write_mean['Throughput (GB/s)']

# Plot Sequential Read Data
plt.figure(figsize=(10, 9))
plt.errorbar(random_read_mean['IO_Size'],
             random_read_mean['Throughput (GB/s)'],
             yerr=[random_read_lower_err, random_read_upper_err],
             label='Sequential Read', marker='o', linestyle='-',
             elinewidth=1, capsize=4, capthick=1)

# Plot Sequential Write Data
plt.errorbar(random_write_mean['IO_Size'],
             random_write_mean['Throughput (GB/s)'],
             yerr=[random_write_lower_err, random_write_upper_err],
             label='Sequential Write', marker='o', linestyle='-',
             elinewidth=1, capsize=4, capthick=1)

plt.xscale('log')
# Define the custom x-axis tick positions and labels
custom_x_ticks = [
    4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
    1048576, 2097152, 4194304, 8388608, 12582912, 16777216, 25165824, 33554432
]
custom_x_labels = [
    '4KB', '8KB', '16KB', '32KB', '64KB', '128KB', '256KB', '512KB',
    '1MB', '2MB', '4MB', '8MB', '12MB', '16MB', '24MB', '32MB'
]

# Set the custom x-axis ticks and labels
plt.xticks(custom_x_ticks, custom_x_labels, rotation=-90)

# Customize the plot
plt.xlabel('I/O Size (Bytes)')
plt.ylabel('Throughput (GB/s)')
if 'sda2' in sys.argv[1]:
    plt.title('Random I/O vs. Throughput w/ 95% CI, /dev/sda2')
elif 'sdb1' in sys.argv[1]:
    plt.title('Random I/O vs. Throughput w/ 95% CI, /dev/sdb1')

plt.grid(True)
plt.legend()

# Show the plot
# Show the plot
if 'sda2' in sys.argv[1]:
    plt.savefig('rand_io_sda2.png')
elif 'sdb1' in sys.argv[1]:
    plt.savefig('rand_io_sdb1.png')

