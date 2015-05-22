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


def print_ls(ls, ident='', braces=1):
    """
    Recursively prints nested lists.

    :param ls: list, arbitrarily nested
    :return: multiline string illustrating structure

    """
    out = ""

    for value in ls:
        if isinstance(value, list):
            out = out + print_ls(value, ident+'\t', braces+1)
        else:  # "leaf" value
            out = out + ident + '{}'.format(value.name if hasattr(value, "name") else value) + '\n'

    return out