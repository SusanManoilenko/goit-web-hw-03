import multiprocessing
from time import time


def factorize_sync(numbers):
    result = []
    for number in numbers:
        factors = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors.append(i)
        result.append(factors)
    return result


def factorize_parallel(numbers):
    with multiprocessing.Pool() as pool:
        return pool.map(factorize_sync, numbers)


def main():
    numbers = [128, 255, 99999, 10651060]

    start_time_sync = time()
    result_sync = factorize_sync(numbers)
    end_time_sync = time()

    print("Sync Execution Time:", end_time_sync - start_time_sync)

    a, b, c, d = result_sync
    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == "__main__":
    main()
