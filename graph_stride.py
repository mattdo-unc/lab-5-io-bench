#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt

# Load the stride data and confidence interval data
if len(sys.argv) != 3:
    print("Usage: python graph_stride.py <stride_data_csv_file> "
          "<ci_data_csv_file>")
    sys.exit(1)

stride_data = pd.read_csv(sys.argv[1])
ci_data = pd.read_csv(sys.argv[2])

# Define the I/O sizes you want to plot (in Bytes)
io_sizes = [4096, 8192, 16384, 32768, 65536, 131072]

# Filter the data for sequential reads and specified I/O sizes
sequential_data = stride_data[(stride_data['Pattern'] == 'sequential') &
                              (stride_data['Operation'] == 'write') &
                              (stride_data['IO_Size'].isin(io_sizes))]

# Filter the confidence interval data for relevant I/O sizes
ci_data = ci_data[(ci_data['Pattern'] == 'sequential') &
                  (ci_data['Operation'] == 'write') &
                  (ci_data['IO_Size'].isin(io_sizes))]

# Define custom colors for different I/O sizes
colors = ['blue', 'green', 'red', 'purple', 'orange', 'pink']

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 9))

# Plot I/O Stride vs. Throughput for different I/O sizes
for i, io_size in enumerate(io_sizes):
    io_data = sequential_data[sequential_data['IO_Size'] == io_size]

    # Filter confidence interval data for the current I/O size
    ci_io_data = ci_data[ci_data['IO_Size'] == io_size]

    # Calculate error bars
    throughput_lower_err = io_data['Throughput (GB/s)'] - ci_io_data[
        'Throughput (GB/s) - Lower CI']
    throughput_upper_err = ci_io_data['Throughput (GB/s) - Upper CI'] - \
                           io_data['Throughput (GB/s)']

    # Plot the data with error bars
    ax.errorbar(io_data['Stride'], io_data['Throughput (GB/s)'],
                yerr=[throughput_lower_err, throughput_upper_err],
                label=f'I/O Size {io_size} Bytes', marker='o', linestyle='-',
                color=colors[i])

# Customize the plot
plt.xscale('log')
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
ax.set_xlabel('I/O Stride (Bytes)')
ax.set_ylabel('Throughput (GB/s)')
if 'sda2' in sys.argv[1]:
    ax.set_title('Rand. Stride Writes vs. Throughput Performance on /dev/sda2')
elif 'sdb1' in sys.argv[1]:
    ax.set_title('Rand. Stride Writes vs. Throughput Performance on /dev/sdb1')
ax.grid(True)
ax.legend()

# Show the plot
# Show the plot
if 'sda2' in sys.argv[1]:
    plt.savefig('seq_writes_stride_sda2.png')
elif 'sdb1' in sys.argv[1]:
    plt.savefig('seq_writes_stride_sdb1.png')

