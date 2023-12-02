# Compiler and Compiler Flags
CC=gcc
CFLAGS=-Wall -Werror -Wextra -O3

# Source files and Object files
SRCS=main.c
OBJS=$(SRCS:.c=.o)

# Target Executable
TARGET=iobench

# Default target
all: $(TARGET)

# Rule for building the target executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# Generic rule for compiling object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Rule for cleaning up generated files
clean:
	rm -f $(TARGET) $(OBJS)
