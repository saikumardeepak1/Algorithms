def insertion_sort(b):
    for i in range(1, len(b)):
        up = b[i]
        j = i - 1
        while j >= 0 and b[j] > up:
            b[j + 1] = b[j]
            j -= 1
        b[j + 1] = up
    return b

def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    # Find maximum value and minimum value to determine bucket range and size
    max_value = max(arr)
    min_value = min(arr)
    bucket_range = max_value - min_value

    if bucket_range == 0:  # All elements are the same
        return arr

    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for i in range(len(arr)):
        # Calculate index of the bucket this element will go to
        index = int(((arr[i] - min_value) / bucket_range) * (bucket_count - 1))
        buckets[index].append(arr[i])

    # Sort individual buckets and concatenate
    final_output = []
    for bucket in buckets:
        insertion_sort(bucket)
        final_output.extend(bucket)

    return final_output