from collections import Counter


def format_ranges(initial):
    start = None
    it = None
    result = []
    sorted_list = sorted(initial)
    c = Counter(sorted_list)
    while c:
        for item, count in c.items():
            if not start:
                start = item
                it = item
            else:
                if item == it + 1:
                    it = item
        result.append((start, it))
        c.subtract({k: 1 for k in range(start, it + 1)})
        start = None
        c += Counter()
    result.sort()
    return ','.join(f"{i}-{j}" if i != j else str(i) for i, j in result)
