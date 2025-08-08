from functools import lru_cache
from splay import SplayTree
import timeit
import matplotlib.pyplot as plt
from colorama import Fore, Style


@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    value = tree.find(n)
    if value is not None:
        return value
    if n < 2:
        return n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def measure_time(func, *args):
    return timeit.timeit(lambda: func(*args), number=10) / 10


def visualize_results(result, n_values):
    lru_times = [result[n][0] for n in n_values]
    splay_times = [result[n][1] for n in n_values]

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, label="LRU Cache", marker="o", color="blue")
    plt.plot(n_values, splay_times, label="Splay Tree", marker="x", color="orange")
    plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
    plt.xlabel("Число Фібоначчі n")
    plt.ylabel("Середній час виконання (секунди)")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    n_values = range(0, 951, 50)
    tree = SplayTree()
    result = {}

    for n in n_values:
        time_lru = measure_time(fibonacci_lru, n)
        time_splay = measure_time(fibonacci_splay, n, tree)
        result[n] = time_lru, time_splay

    print(
        f"{Fore.RED}{'n':<5} {'LRU Cache Time (s)':<20} {'Splay Tree Time (s)':<20}{  Style.RESET_ALL}"
    )
    print(Fore.RED + "-" * 45 + Style.RESET_ALL)
    for n in n_values:
        time_lru, time_splay = result[n]
        print(f"{n:<6}{time_lru:<21.8f}{time_splay:<20.8f}")

    visualize_results(result, n_values)


if __name__ == "__main__":
    main()
