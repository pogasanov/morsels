from itertools import zip_longest

sentinel = object()


def interleave(*el):
    for zipped in zip_longest(*el, fillvalue=sentinel):
        yield from (
            item
            for item in zipped
            if item is not sentinel
        )
