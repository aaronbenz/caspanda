###################################################
#################[ Module: Utils ]#################
###################################################
"""
Miscellaneous utilities for caspanda.
"""


def paste(x, sep=", "):
    """
    Custom string formatting function to format (???) output.
    """

    return str(x).strip("[]").replace("'","").replace(", ", sep)