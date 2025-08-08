import random
from lru_cache import LRUCache
import time


def range_sum_no_cache(array, left, right):
    """Обчислює суму елементів масиву від left до right без кешування."""
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    """Оновлює значення елемента масиву за індексом без кешування."""
    if 0 <= index < len(array):
        array[index] = value
    else:
        raise IndexError("Неправильний індекс для оновлення")


def range_sum_with_cache(array, left, right, cache):
    """Обчислює суму елементів масиву від left до right з кешуванням."""
    key = (left, right)
    result = cache.get(key)
    if result == -1:
        result = sum(array[left : right + 1])
        cache.put(key, result)
    return result


def update_with_cache(array, index, value, cache):
    array[index] = value
    keys_to_invalidate = [key for key in cache.cache if key[0] <= index <= key[1]]
    for key in keys_to_invalidate:
        del cache.cache[key]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% запитів — Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% — Range
            if random.random() < p_hot:  # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:  # 5% — випадкові діапазони
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


def process_queries_no_cache(array, queries):
    for query in queries:
        if query[0] == "Update":
            update_no_cache(array, query[1], query[2])
        else:
            range_sum_no_cache(array, query[1], query[2])


def process_queries_with_cache(array, queries, cache):
    for query in queries:
        if query[0] == "Update":
            update_with_cache(array, query[1], query[2], cache)
        else:
            range_sum_with_cache(array, query[1], query[2], cache)


def run_with_timing(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    elapsed = end - start
    return elapsed


def main():
    n = 100000
    q = 50000
    queries = make_queries(n, q)
    array = [random.randint(1, 100) for _ in range(n)]
    array_no_cache = array.copy()
    array_with_cache = array.copy()
    cache = LRUCache(1000)  # Кеш на 1000 елементів

    time_no_cache = run_with_timing(process_queries_no_cache, array_no_cache, queries)
    time_with_cache = run_with_timing(
        process_queries_with_cache, array_with_cache, queries, cache
    )

    print(f"{'Без кешу':<8} {':':<1} {time_no_cache} c")
    print(
        f"{'LRU-кеш':<8} {':':<1} {time_with_cache} c (прискорення x{time_no_cache / time_with_cache:.1f})"
    )


if __name__ == "__main__":
    main()
