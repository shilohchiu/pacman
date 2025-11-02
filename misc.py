"""
helper functions
"""

def float_range(start, stop, step):
    """
    range helper function for pellets
    """
    while start < stop:
        yield start
        start += step
