"""
This file is meant to some valuable information about a cassandra table
"""
from caspanda.utils import paste, print_ls

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
    # TODO: add the rest of arguments

    def __init__(self, keyspace_name, columnfamily_name, column_name, component_index=None, index_name=None, index_options=None, index_type=None, cql_type=None, validator=None):
        self.keyspace = keyspace_name
        self.table = columnfamily_name
        self.name = column_name
        self.component_index = component_index
        self.index_name = index_name
        self.index_options = index_options
        self.index_type = index_type
        self.cql_type = cql_type

    def describe(self):
        """
        Describes the column in a print friendly manner
        :return:
        """
        pass
class TableMeta(object):
    keyspace = None
    name = None
    columns = {}


    def __init__(self, keyspace_name, name, columns=None):
        self.keyspace = keyspace_name
        self.name = name
        self.columns = {} if columns is None else columns

    def add_column(self, x):
        self.columns.append(x)

    def describe(self, *args, **kwargs):
        """ Recursively prints nested lists."""
        return print_ls(self.categorize_columns())

    def sort_columns(self, x, reverse = False):
        seq = []
        for i in x:
            seq.append((i.component_index, i))
        seq.sort(reverse=reverse)
        return [x[1] for x in seq]

    def categorize_columns(self):
        partition_cols = []
        clustering_cols = []
        regular_cols = []
        static_cols = []

        for i in self.columns.itervalues():
            if i.cql_type == "partition_key":
                partition_cols.append(i)
                next
            if i.cql_type == "clustering_key":
                clustering_cols.append(i)
                next
            if i.cql_type == "regular":
                regular_cols.append(i)
                next
            if i.cql_type == "static":
                static_cols.append(i)
                next

        partition_cols = self.sort_columns(partition_cols)
        clustering_cols = self.sort_columns(clustering_cols, reverse=True)
        cluster_str = regular_cols
        for i in clustering_cols:
            cluster_str = [i, cluster_str]

        partition_cols = paste([i.name for i in partition_cols])

        return partition_cols,[cluster_str, static_cols]

#TODO utilize TableMeta.describe to implement the same thing for keyspaces
class KeyspaceMeta(object):
    name = None
    tables = {}
    # TODO: fill in the rest of the arguments for keyspace

    def __init__(self, name, tables=None):
        self.name = name
        self.tables = {} if tables is None else tables

    def add_table(self, x):
        self.tables.append(x)


