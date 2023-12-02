#!/bin/bash

# Define the range of I/O sizes, strides, and granularities

# 4kB to 100MB
io_sizes=("4096" "8192" "16384" "32768" "65536" "131072" "262144" "524288" "1048576" "2097152" "4194304" "8388608" "16777216" "33554432" "67108864" "134217728" "268435456" "536870912" "1073741824")
# 4kB to 10MB
strides=("4096" "8192" "16384" "32768" "65536" "131072" "262144" "524288" "1048576" "2097152" "4194304" "8388608" "10485760")
operations=("read" "write")
patterns=("sequential" "random")
devices=("testfile.img" "/dev/sdb") # HDD and SSD

# Function to run benchmark
run_benchmark() {
    local device=$1
    local io_size=$2
    local stride=$3
    local operation=$4
    local pattern=$5

    ./iobench -d "$device" -s "$io_size" -t "$stride" -o "$operation" -p "$pattern"
}

# Main loop for all combinations
for device in "${devices[@]}"; do
    for operation in "${operations[@]}"; do
        for io_size in "${io_sizes[@]}"; do
            # I/O Size Test
            run_benchmark "$device" "$io_size" "0" "$operation" "sequential"

            # I/O Stride Test
            for stride in "${strides[@]}"; do
                run_benchmark "$device" "$io_size" "$stride" "$operation" "sequential"
            done

            # Random I/O Test
            run_benchmark "$device" "$io_size" "0" "$operation" "random"
        done
    done
done
