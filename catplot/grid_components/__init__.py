import functools

# Decorators used in grid plotting components.

def extract_plane(func):
    """ A decorator constructor to correct the plane name before
        grid component mapping.
    """
    @functools.wraps(func)
    def _extract_plane(*args, **kwargs):
        plane = kwargs.get("plane", "xy")
        kwargs["plane"] = "".join(sorted(plane))
        return func(*args, **kwargs)
    return _extract_plane

