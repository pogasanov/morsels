from collections import Counter


def format_ranges(initial):
    start = end = None
    result = []
    sorted_list = sorted(initial)
    c = Counter(sorted_list)
    while c:
        for item in c.keys():
            if not start:
                start = end = item
            else:
                if item == end + 1:
                    end = item
        result.append((start, end))
        c.subtract({k: 1 for k in range(start, end + 1)})
        start = None
        c += Counter()
    result.sort()
    return ','.join(f"{i}-{j}" if i != j else str(i) for i, j in result)
