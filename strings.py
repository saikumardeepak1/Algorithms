import random
import time
import matplotlib.pyplot as plt
from Quick_Sort import quick_sort
from Heap_Sort import heap_sort
from Merge_Sort import merge_sort
from Radix_Sort import radix_sort
from Bucket_Sort import bucket_sort
from Tim_Sort import tim_sort
import string

# Generating Arrays of Random Strings
def generate_array_random_strings(n, length=5):
    return [''.join(random.choices(string.ascii_lowercase, k=length)) for _ in range(n)]

# Measuring Sorting Time
def measure_time(sorting_function, arr):
    start_time = time.time()
    sorting_function(arr)  # Use a copy to avoid modifying the original array
    return time.time() - start_time

# Function to run tests and plot results
def run_tests_and_plot(sorting_functions, array_generator, sizes):
    time_results = {sort_name: [] for sort_name in sorting_functions}

    # Plotting Line Graphs
    plt.figure(figsize=(10, 6))
    for sort_name, sort_function in sorting_functions.items():
        times = [measure_time(sort_function, array_generator(n)) for n in sizes]
        time_results[sort_name] = times
        plt.plot(sizes, times, label=sort_name, linewidth=2.5)

    plt.xlabel('Size of Array')
    plt.ylabel('Time to Sort (seconds)')
    plt.title('Sorting Performance with Random Strings')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plotting Bar Charts
    avg_times = []
    for sort_name in sorting_functions:
        times_for_sizes = [time_results[sort_name][size_idx] for size_idx in range(len(sizes))]
        avg_times.append(sum(times_for_sizes) / len(times_for_sizes))

    plt.figure()
    for sort_name in sorting_functions:
        avg_time = sum(time_results[sort_name]) / len(sizes)
        plt.bar(sort_name, avg_time,label=sort_name)

    plt.xlabel('Sorting Algorithm')
    plt.ylabel('Average Time to Sort (seconds)')
    plt.title(f'Average Sorting Time Comparison')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    # Printing the array type being sorted
    print("Array Type: Random Strings")
    for size in sizes:
        array_printout = array_generator(size)
        print(f"Size {size}: {array_printout if len(array_printout) <= 10 else array_printout[:10] + ['...']}")

# Define sorting functions
sorting_functions = {
    'Quick Sort': quick_sort,
    'Heap Sort': heap_sort,
    'Merge Sort': merge_sort,
    # 'Radix Sort': radix_sort,  # Excluded for string test
    #'Bucket Sort': bucket_sort,
    'Tim Sort': tim_sort
}

# Define array sizes to test
sizes = [100000, 200000, 300000, 400000, 500000]  # Adjust based on your needs

# Run the tests and plot with random strings
run_tests_and_plot(sorting_functions, generate_array_random_strings, sizes)
