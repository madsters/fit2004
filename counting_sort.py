def counting_sort(arr = []):
    count_range = max(arr) + 1
    count_arr = [0]*count_range
    pos_arr = [0]*count_range
    sorted_arr = [0]*len(arr)

    '''
    creating count of each number
    '''
    for i in arr:
        count_arr[i] += 1

    '''
    getting position array
    '''
    for i, j in enumerate(count_arr):
        if i == len(count_arr) - 1:
            continue
        pos_arr[i+1] = pos_arr[i] + j
    
    '''
    creating new sorted array
    '''
    for i,j in enumerate(arr):
        sorted_arr[pos_arr[j]] = j
        pos_arr[j] += 1

    return sorted_arr

def main():
    arr = [3, 6, 5, 4, 8, 3, 2, 9, 4, 5, 7, 2, 1]
    print(counting_sort(arr))

if __name__ == "__main__":
    main()
