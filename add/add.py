from itertools import zip_longest

fillvalue = object()


def add(*args):
    try:
        return sum(args)
    except TypeError:
        summed_result = []
        for zipped in zip_longest(*args, fillvalue=fillvalue):
            if fillvalue in zipped:
                raise ValueError("Given matrices are not the same size.")
            summed_result.append(add(*zipped))
        return summed_result
