"""
A Panda has spots, and so does data. This is meant to define ways to more easily view caspanda data
"""

from cassandra.metadata import TableMetadata, KeyspaceMetadata
from exceptions import InputError

def describe(x):
    """
    Given a TableMetaData or list of KeyspaceMetaData, it will return a description of all of the tables in that Keyspace. Given a
    TableMetaData or a list of TableMetaData, it will return the description of all of them
    :param x: A list or a single keyspace/table
    :return: A json description of the tables
    """

    raise(InputError)
    pass


