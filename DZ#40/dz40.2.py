import multiprocessing
import time

def calculate_fuctorial(n):
    result = 1
    for i in range(1, n + 1):
        print(i)
        print(result)
        result *= i
        print("")
    
    return result

def factorials_in_parallel(numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(calculate_fuctorial, numbers)
    return results

if __name__ == "__main__":
    numbers = list(range(1, 10))
    start_time = time.time()
    results_parallel = factorials_in_parallel(numbers)
    end_time = time.time()
    parallel_time = end_time - start_time

    print(f"lead time with multitasking{parallel_time:.4f} sec")

    start_time = time.time()
    results_seq = [calculate_fuctorial(n) for n in numbers]
    end_time = time.time()
    seq_time = end_time - start_time

    print(f"lead time with out multitasking {seq_time:.4f} sec")

    print(f"with multitasking  {results_parallel[:5]}")
    print(f"with out multitasking  {results_seq[:5]}")