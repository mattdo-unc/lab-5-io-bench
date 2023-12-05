//
// Created by mattdo on 12/5/23.
//
#include <stdio.h>
#include <stdlib.h>

void calculate_midpoints(int min, int max, int granularity, int* result, int* count) {
    int mid = (min + max) / 2;
    if (mid - min > granularity) {
        result[*count] = mid;
        (*count)++;
        calculate_midpoints(min, mid, granularity, result, count);
        calculate_midpoints(mid, max, granularity, result, count);
    }
}

int compare(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

void print_array(int* arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d\n", arr[i]);
    }
}

int main() {
    int io_min = 4096;      // 4KB
    int io_max = 104857600; // 100MB
    int stride_min = 4096;  // 4KB
    int stride_max = 104857600; // 100MB
    int granularity = 1048576; // 1MB
    int io_sizes[100] = {io_min, io_max}; // Large enough array
    int strides[100] = {stride_min, stride_max}; // Large enough array
    int io_count = 2, stride_count = 2;

    calculate_midpoints(io_min, io_max, granularity, io_sizes, &io_count);
    calculate_midpoints(stride_min, stride_max, granularity, strides, &stride_count);

    qsort(io_sizes, io_count, sizeof(int), compare);
    qsort(strides, stride_count, sizeof(int), compare);

    printf("IO Sizes:\n");
    print_array(io_sizes, io_count);

    printf("\nStrides:\n");
    print_array(strides, stride_count);

    return 0;
}
