#!/bin/bash

# Define the range of I/O sizes, strides, and granularities

# I/O Sizes in bytes: 4KB to 100MB
io_sizes=(
    "4096"        # 4KB
    "8192"        # 8KB
    "16384"       # 16KB
    "32768"       # 32KB
    "65536"       # 64KB
    "131072"      # 128KB
    "262144"      # 256KB
    "524288"      # 512KB
    "1048576"     # 1MB
    "2097152"     # 2MB
    "4194304"     # 4MB
    "8388608"     # 8MB
    "16777216"    # 16MB
    "33554432"    # 32MB
    "67108864"    # 64MB
    "104857600"   # 100MB
)

# Stride Sizes in bytes: 4KB to 100MB
strides=(
    "4096"        # 4KB
    "8192"        # 8KB
    "16384"       # 16KB
    "32768"       # 32KB
    "65536"       # 64KB
    "131072"      # 128KB
    "262144"      # 256KB
    "524288"      # 512KB
    "1048576"     # 1MB
    "2097152"     # 2MB
    "4194304"     # 4MB
    "8388608"     # 8MB
    "16777216"    # 16MB
    "33554432"    # 32MB
    "67108864"    # 64MB
    "104857600"   # 100MB
)

operations=("read" "write")
patterns=("sequential" "random")
# devices=("/dev/sdb1" "/dev/sda2") # HDD and SSD
devices=("testfile.img") # HDD and SSD
output_file="benchmark_results.csv"

run_benchmark() {
    local device=$1
    local io_size=$2
    local stride=$3
    local operation=$4
    local pattern=$5
    local run_number=$6

    # Execute the benchmark and capture its output
    result=$(./iobench -d "$device" -s "$io_size" -t "$stride" -o "$operation" -p "$pattern")

    echo "$device, $io_size, $stride, $operation, $pattern, $run_number, $result" >> $output_file
}

# Initialize the output file with headers
echo "Device, IO_Size, Stride, Operation, Pattern, Time (s), Throughput (GB/s)" > $output_file
# Main loop for all combinations
for device in "${devices[@]}"; do
    for operation in "${operations[@]}"; do
        for io_size in "${io_sizes[@]}"; do
            for stride in "${strides[@]}"; do
                for pattern in "${patterns[@]}"; do
                    for run in {1..5}; do
                        run_benchmark "$device" "$io_size" "$stride" "$operation" "$pattern" "$run"
                    done
                done
            done
        done
    done
done
