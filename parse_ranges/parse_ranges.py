def parse_ranges(input_string):
    for range_of_numbers in input_string.split(','):
        try:
            a, b = range_of_numbers.split('-')
        except ValueError:
            yield int(range_of_numbers)
        else:
            if b == '>exit':
                yield int(a)
            else:
                for x in range(int(a), int(b) + 1):
                    yield x
