#!/bin/bash

# Set up a temporary disk image for safe benchmarking
IMAGE_FILE="test.img"
IMAGE_SIZE_MB=1024 # 1 GB
LOOP_DEVICE=""

# Function to create a disk image
create_disk_image() {
    echo "Creating $IMAGE_SIZE_MB MB disk image..."
    dd if=/dev/zero of=$IMAGE_FILE bs=1M count=$IMAGE_SIZE_MB
}

# Function to set up a loop device
setup_loop_device() {
    echo "Setting up loop device..."
    LOOP_DEVICE=$(sudo losetup -fP --show $IMAGE_FILE)
    echo "Loop device $LOOP_DEVICE created."
}

# Function to run the benchmark
run_benchmark() {
    # Example benchmark command - modify according to your needs
    echo "Running benchmark on $LOOP_DEVICE..."
    sudo ./iobench -d $LOOP_DEVICE -s 4096 -t 0 -o read -p sequential
}

# Function to clean up: detach loop device and remove image file
cleanup() {
    echo "Cleaning up..."
    if [ -n "$LOOP_DEVICE" ]; then
        sudo losetup -d $LOOP_DEVICE
        echo "Loop device $LOOP_DEVICE detached."
    fi
    rm -f $IMAGE_FILE
    echo "Disk image removed."
}

# Main script execution
create_disk_image
setup_loop_device
run_benchmark
cleanup

echo "Benchmarking completed."
