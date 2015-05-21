"""
This file is meant to some valuable information about a cassandra table
"""

from caspanda.bear import CasPanda

class ColumnMeta(object):
    keyspace = None
    """
    The keypace the column belongs to
    """

    table = None
    """
    The table the column belongs to
    """

    name = None
    """
    The name of the column
    """
    ###Todo add the rest of arguments

    def __init__(self, keyspace_name, columnfamily_name, column_name, component_index=None, index_name=None, index_options=None, index_type=None, cql_type=None):
        self.keyspace = keyspace_name
        self.table = columnfamily_name
        self.name = column_name
        self.component_index = component_index
        self.index_name = index_name
        self.index_options = index_options
        self.index_type = index_type
        self.cql_type = cql_type

    def _sync(self):
        """
        using the keyspace, table, and name, syncs the rest of the column values
        :return: None
        """
        pass

    def describe(self):
        """
        Describes the column in a print friendly manner
        :return:
        """
        pass


class TableMeta(object):
    keyspace = None
    name = None
    ###Todo fill in the rest of the TableMeta arguments

    def __init__(self, keyspace_name, columnfamily_name, columns=None):
        self.keyspace = keyspace_name
        self.name = columnfamily_name
        self.columns = [] if columns is None else columns

    def get_partition_keys(self):
        """
        Gets the partition keys based off of the ColumnMeta object's "type" variable == "partition_key"
        :return:
        """
        pass

    def _sync(self):
        """
        Syncs up the TableMeta with the information in Cassandra based on the keyspace and table name
        :return:
        """
        pass

    def describe(self):
        """
        Describes the table in a print friendly manner
        :return:
        """
        pass

class KeyspaceMeta(object):
    name = None
    tables = None
    ###Todo fill in the rest of the arguments for keyspace

    def __init__(self, name):
        self.name = name

    def _sync(self):
        """
        Sync up the Keyspace with the information in Cassandra based on the keyspace name
        :return:
        """
        pass

    def describe(self):
        """
        Describes the keyspace's tables in a print friendly manner
        :return:
        """
        pass


