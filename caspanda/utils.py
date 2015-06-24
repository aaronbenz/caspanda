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
    out = ""
    for i in x:
        out += i + sep
    return out.strip(sep)

def print_ls(ls, ident = '', braces=1):
    """ Recursively prints nested lists."""
    out = ""
    for value in ls:
        if isinstance(value, list):
            out = out + print_ls(value, ident+'\t', braces+1)
        else:
            #out = out + ident+'%s' %(value if isinstance(value, basestring) else value.name) + '\n'
            out = out + ident+'%s' %(value) + '\n'

    return out

def is_instance_multiple(x, obj_class):
    """
    Checks isinstance of multiple objects to save time. Does nothing if it is none
    :param x: objects
    :param obj_class: class of object
    :return:
    """
    assert isinstance(x, list)
    assert isinstance(obj_class, list)
