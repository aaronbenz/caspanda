###################################################
#################[ Module: Utils ]#################
###################################################
"""
Miscellaneous utilities for caspanda.
"""
import caspanda.metabear

def paste(x, sep=", "):
    """
    Custom string formatting function to format (???) output.
    """
    return str(x).strip("[]").replace("'","").replace(", ", sep)

def print_ls(ls, ident = '', braces=1):
    """ Recursively prints nested lists."""
    out = ""
    for value in ls:
        if isinstance(value, list):
            out = out + print_ls(value, ident+'\t', braces+1)
        else:
            out = out + ident+'%s' %(value.name if isinstance(value, caspanda.metabear.ColumnMeta) else value) + '\n'
    return out