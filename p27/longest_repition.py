def longest_repetition(input_list):
    best = None
    best_length = 0
    current = None
    current_length = 0
    for i in input_list:
        if i != current:
            current = i
            current_length = 1
        else:
            current_length += 1
        if current_length > best_length:
            best_length = current_length
            best = current
    return best

print longest_repetition([1, 2, 2, 3, 3, 3, 2, 2, 1])
# 3

print longest_repetition(['a', 'b', 'b', 'b', 'c', 'd', 'd', 'd'])
# b

print longest_repetition([1,2,3,4,5])
# 1

print longest_repetition([])
# None