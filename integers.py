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

# Generating Different Types of Input Arrays
def generate_array_random_integers(n):
    return [random.randint(0, n) for _ in range(n)]

def generate_array_random_integers_range_k(n, k=1000):
    return [random.randint(0, k) for _ in range(n)]

def generate_array_random_integers_n3(n):
    return [random.randint(0, n**3) for _ in range(n)]

def generate_array_random_integers_logn(n):
    return [random.randint(0, int(math.log2(n) + 1)) for _ in range(n)]

def generate_array_multiples_of_1000(n):
    return [random.randint(0, n) * 1000 for _ in range(n)]

def generate_array_swapped(n):
    arr = list(range(n))
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
        plt.figure()
        for sort_name, sort_function in sorting_functions.items():
            times = [measure_time(sort_function, generator(n)) for n in sizes]
            time_results[sort_name] = times
            plt.plot(sizes, times, label=sort_name)

        plt.xlabel('Size of Array')
        plt.ylabel('Time to Sort (seconds)')
        plt.title(f'Sorting Performance: {name}')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Printing the array type being sorted
        print(f"Array Type: {name}")
        for size in sizes:
            print(f"Size {size}: {generator(size)}")

        # Plotting Bar Charts
        avg_times = []
        for sort_name in sorting_functions:
            times_for_sizes = [time_results[sort_name][size_idx] for size_idx in range(len(sizes))]
            avg_times.append(sum(times_for_sizes) / len(times_for_sizes))

        plt.figure()
        for sort_name in sorting_functions:
            avg_time = sum(time_results[sort_name]) / len(sizes)
            plt.bar(sort_name, avg_time)

        plt.xlabel('Sorting Algorithm')
        plt.ylabel('Average Time to Sort (seconds)')
        plt.title(f'Average Sorting Time Comparison: {name}')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    # Main Function to Run Tests and Plot Results

    # Define array sizes to test
    # Define sorting functions
sorting_functions = {
        'Quick Sort': quick_sort,
        'Heap Sort': heap_sort,
        'Merge Sort': merge_sort,
        'Radix Sort': radix_sort,
        'Bucket Sort': bucket_sort,  # Ensure correct name is used here
        'Tim Sort': tim_sort}


# Define array generators
array_generators = {
    'Random Integers [0...n]': generate_array_random_integers,
    'Random Integers [0...k]': generate_array_random_integers_range_k,
    'Random Integers [0...n^3]': generate_array_random_integers_n3,
    'Random Integers [0...log n]': generate_array_random_integers_logn,
    'Multiples of 1000 [0...n]': generate_array_multiples_of_1000,
    'Swapped [0...n]': generate_array_swapped
}

sizes = [100000, 200000, 300000, 400000, 500000]  # Adjust based on your needs

# Run the tests and plot
run_tests_and_plot(sorting_functions, array_generators, sizes)
