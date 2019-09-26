from itertools import zip_longest


def add(*args):
    fillvalue = object()
    response = []
    for zipped in zip_longest(*args, fillvalue=fillvalue):
        if fillvalue in zipped:
            raise ValueError()
        inp = []
        for items in zip_longest(*zipped, fillvalue=fillvalue):
            if fillvalue in items:
                raise ValueError()
            inp.append(sum(items))
        response.append(inp)
    return response
