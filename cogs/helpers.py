"""
Helper functions for Epsilon. Not intended to be a cog.
"""


def represents_int(string):
    """
    Checks whether a string is an integer
    """
    try:
        int(string)
        return True
    except ValueError:
        return False
