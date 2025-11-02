"""
helper functions
"""

# range helper function for pellets 
def float_range(start, stop, step):
     while start < stop:
          yield start
          start += step 