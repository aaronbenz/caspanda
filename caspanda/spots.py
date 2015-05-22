###################################################
#################[ Module: Spots ]#################
###################################################
"""
A Panda has spots, and so does data. 

This module provides utilities for pretty-printing and exposing the internal structure of data fetched from Cassandra.
"""
from cassandra.metadata import TableMetadata
from cassandra.metadata import KeyspaceMetadata

from caspanda.exceptions import InputError


def describe(x):
    """
    Given a TableMetaData or list of KeyspaceMetaData, it will return a description of all of the tables in that Keyspace. Given a
    TableMetaData or a list of TableMetaData, it will return the description of all of them
    :param x: A list or a single keyspace/table
    :return: A json description of the tables
    """

    raise(InputError)
    pass


def _describe_table(x):
    """
    Describes a single TableMetaData table
    :param x: TableMetaData
    :return: dict describing x layout
    """



