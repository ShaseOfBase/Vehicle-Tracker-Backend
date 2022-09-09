import math

def get_next_smallest(array, num):
    if not isinstance(num, int):
        return -1

    array.sort()

    next_smallest = None

    for i in range(len(array)):
        if array[i] == num:
            return num

        if array[i] - num < 0:
            next_smallest = array[i]
        elif array[i] - num > 0:  # We've passed our target
            if not next_smallest:
                next_smallest = array[i]
            break

    return next_smallest


if __name__ == '__main__':
    arr = [3, 4, 6, 9, 10, 12, 14, 15, 17, 19, 21]
    num = 11
    print(get_next_smallest(arr, num))
