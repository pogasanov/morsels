def deep_flatten(items):
    try:
        for item in items:
            if isinstance(item, str):
                yield item
            else:
                yield from deep_flatten(item)
    except TypeError:
        yield items
