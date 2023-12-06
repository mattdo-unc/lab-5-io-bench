/*
 * mattdo-unc
 * 730406661
 *
 * Microbenchmark Utility for Disk I/O Performance Analysis with getopt
 *
 * This utility measures and analyzes the performance of disk I/O operations
 * under various conditions and patterns. Ensure that you have sufficient
 * permissions to perform READ/WRITE operations on the specified device/file.
 *
 * Command-Line Options:
 *  -d <device>       : Specify the device file (e.g., /dev/sda).
 *  -s <size>         : Size of each I/O operation in bytes (e.g., 4096 for 4KB).
 *  -t <stride>       : Stride size in bytes between I/O operations.
 *  -o <operation>    : I/O operation type: 'read' or 'write'.
 *  -p <pattern>      : I/O pattern: 'sequential' or 'random'.
 *  -h                : Display help information and exit.
 *
 * Usage Examples:
 *  - Sequential Writes with 4KB Blocks: ./iobench -d /dev/sda -s 4096 -t 0 -o write -p sequential
 *  - Random Reads with 8KB Blocks: ./iobench -d /dev/sda -s 8192 -t 0 -o read -p random
 *  - Display Help: ./iobench -h
 *
 * Notes:
 * - Replace /dev/sda with the appropriate device file for your testing environment.
 * - Exercise caution with the chosen device and operations, especially write operations that modify data.
 * - Ensure necessary permissions are obtained for performing these operations on the specified device.
 * - The utility assumes a total data size of 1 GB for its calculations and throughput measurements.
 *
 * For test purposes, we can create a 1GB file named testfile.img:
 *      dd if=/dev/zero of=testfile.img bs=1G count=1
 */


#define _GNU_SOURCE
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>

#define KB4 (4 * 1024)
#define GB (32 * 1024 * 1024)

void perform_io(const char *device, size_t io_size, size_t stride, int is_read, int is_random) {
    // Open the device file with direct I/O access.
    int fd = open(device, O_SYNC | O_DIRECT | O_LARGEFILE | (is_read ? O_RDONLY : O_WRONLY));
    if (fd < 0) {
        perror("Error opening device");
        exit(EXIT_FAILURE);
    }

    // Allocate aligned memory for I/O operations; alignment = 4kB
    void *buffer;
    if (posix_memalign(&buffer, KB4, io_size)) {
        perror("Error allocating aligned memory");
        close(fd);
        exit(EXIT_FAILURE);
    }

    // Initialize the buffer: fill with 0 for read, 1 for write.
    memset(buffer, is_read ? 0 : 1, io_size);

    size_t total_written = 0;
    struct timeval start, end;
    ssize_t ret;

    gettimeofday(&start, NULL);
    while (total_written < GB) {
        if (is_random) {
            // Random offset for random I/O
            off_t offset = ((off_t) rand() % (GB / io_size)) * io_size;
            lseek(fd, offset, SEEK_SET);
        }

        if (is_read) {
            ret = read(fd, buffer, io_size);
            if (ret < 0) {
                perror("Read error");
                free(buffer);
                close(fd);
                exit(EXIT_FAILURE);
            }
        } else {
            ret = write(fd, buffer, io_size);
            if (ret < 0) {
                perror("Write error");
                free(buffer);
                close(fd);
                exit(EXIT_FAILURE);
            }
        }

        total_written += io_size;

        // Add stride for non-random I/O
        if (!is_random && stride > 0) {
            lseek(fd, stride, SEEK_CUR);
        }
    }

    fsync(fd);
    gettimeofday(&end, NULL);

    double elapsed = (end.tv_sec - start.tv_sec) + ((end.tv_usec - start.tv_usec) / 1000000.0);
    printf("%.10f,%.10f\n", elapsed, 1 / elapsed);

    free(buffer);
    close(fd);
}

void print_usage() {
    printf("Usage: ./iobench -d <device> -s <size> -t <stride> -o <operation> -p <pattern>\n");
    printf("Options:\n");
    printf("  -d <device>       Specify the device file (e.g., /dev/sda)\n");
    printf("  -s <size>         Size of each I/O operation in bytes\n");
    printf("  -t <stride>       Stride size in bytes between I/O operations\n");
    printf("  -o <operation>    I/O operation type: read or write\n");
    printf("  -p <pattern>      I/O pattern: sequential or random\n");
    printf("  -h                Display this help message\n\n");
    printf("Example:\n  ./iobench -d /dev/sda -s 4096 -t 4096 -o write -p sequential\n");
}

int main(int argc, char **argv) {
    int opt;
    char *device = NULL;
    size_t io_size = 0, stride = 0;
    int is_read = 0, is_random = 0;

    while ((opt = getopt(argc, argv, "d:s:t:o:p:h")) != -1) {
        switch (opt) {
            case 'd':
                device = optarg;
                break;
            case 's':
                io_size = atol(optarg);
                break;
            case 't':
                stride = atol(optarg);
                break;
            case 'o':
                is_read = strcmp(optarg, "read") == 0;
                break;
            case 'p':
                is_random = strcmp(optarg, "random") == 0;
                break;
            case 'h':
                print_usage();
                return EXIT_SUCCESS;
            default: /* '?' */
                print_usage();
                return EXIT_FAILURE;
        }
    }

    if (!device || io_size == 0) {
        fprintf(stderr, "Missing required arguments\n");
        print_usage();
        return EXIT_FAILURE;
    }

    perform_io(device, io_size, stride, is_read, is_random);
    return EXIT_SUCCESS;
}
