import random
import time
import math
import matplotlib.pyplot as plt
from Quick_Sort import quick_sort
from Heap_Sort import heap_sort
from Merge_Sort import merge_sort
from Radix_Sort import radix_sort
from Bucket_Sort import bucket_sort
from Tim_Sort import tim_sort

# Generating Different Types of Input Arrays of Floats
def generate_array_random_floats(n, range_max=1.0):
    return [random.uniform(0, range_max) for _ in range(n)]

def generate_array_random_floats_range_k(n, k=1000.0):
    return [random.uniform(0, k) for _ in range(n)]

def generate_array_random_floats_n3(n):
    return [random.uniform(0, n**3) for _ in range(n)]

def generate_array_random_floats_logn(n):
    return [random.uniform(0, math.log2(n) + 1) for _ in range(n)]

def generate_array_multiples_of_1000_floats(n):
    return [random.uniform(0, n) * 1000.0 for _ in range(n)]

def generate_array_swapped_floats(n):
    arr = [float(i) for i in range(n)]
    for _ in range(int(math.log2(n) / 2)):
        a, b = random.sample(range(n), 2)
        arr[a], arr[b] = arr[b], arr[a]
    return arr

# Measuring Sorting Time
def measure_time(sorting_function, arr):
    start_time = time.time()
    sorting_function(arr.copy())  # Use a copy to avoid modifying the original array
    return time.time() - start_time

# Function to aggregate time measurements
def run_tests_and_plot(sorting_functions, array_generators, sizes):
    for name, generator in array_generators.items():
        time_results = {sort_name: [] for sort_name in sorting_functions}

        # Plotting Line Graphs
        plt.figure(figsize=(10, 6))
        for sort_name, sort_function in sorting_functions.items():
            times = [measure_time(sort_function, generator(n)) for n in sizes]
            time_results[sort_name] = times
            plt.plot(sizes, times, label=sort_name, linewidth=2.5)

        plt.xlabel('Size of Array')
        plt.ylabel('Time to Sort (seconds)')
        plt.title(f'Sorting Performance for float datatype: {name}')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Printing the array type being sorted
        print(f"Array Type: {name}")
        for size in sizes:
            array_printout = generator(size)
            print(f"Size {size}: {array_printout if len(array_printout) <= 10 else array_printout[:10] + ['...']}")

# Define sorting functions
sorting_functions = {
    'Quick Sort': quick_sort,
    'Heap Sort': heap_sort,
    'Merge Sort': merge_sort,
    #'Radix Sort': radix_sort,
    'Bucket Sort': bucket_sort,
    'Tim Sort': tim_sort
}

# Define array generators for floats
array_generators = {
    'Random Floats [0...n]': generate_array_random_floats,
    'Random Floats [0...k]': generate_array_random_floats_range_k,
    'Random Floats [0...n^3]': generate_array_random_floats_n3,
    'Random Floats [0...log n]': generate_array_random_floats_logn,
    'Multiples of 1000 [0...n]': generate_array_multiples_of_1000_floats,
    'Swapped [0...n]': generate_array_swapped_floats
}

sizes = [100000]  # Adjust based on your needs

# Run the tests and plot
run_tests_and_plot(sorting_functions, array_generators, sizes)
