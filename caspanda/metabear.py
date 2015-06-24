"""
This file is meant to some valuable information about a cassandra table
"""
from caspanda.utils import paste, print_ls
from cassandra.cqltypes import lookup_casstype
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
        self.validator = validator

    def __repr__(self):
        return "{0} {1} {2}".format(self.name, lookup_casstype(self.validator).typename, self.cql_type if self.cql_type!="regular" else "")

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

    def __repr__(self, *args, **kwargs):
        """ Recursively prints nested lists."""
        return print_ls(self.categorize_columns())

    def sort_columns(self, x, reverse = False):
        seq = []
        for i in x:
            seq.append((i.component_index, i))
        seq.sort(reverse=reverse)
        return [x[1] for x in seq]

    def categorize_columns(self):
        self.partition_cols = []
        self.clustering_cols = []
        self.regular_cols = []
        self.static_cols = []

        for i in self.columns.itervalues():
            if i.cql_type == "partition_key":
                self.partition_cols.append(i)
                next
            if i.cql_type == "clustering_key":
                self.clustering_cols.append(i)
                next
            if i.cql_type == "regular":
                self.regular_cols.append(i)
                next
            if i.cql_type == "static":
                self.static_cols.append(i)
                next

        self.partition_cols = self.sort_columns(self.partition_cols)
        self.clustering_cols = self.sort_columns(self.clustering_cols, reverse=True)
        cluster_str = self.regular_cols
        for i in self.clustering_cols:
            cluster_str = [i, cluster_str]

        #partition_cols = paste([i.name for i in partition_cols])

        return self.partition_cols,[cluster_str, self.static_cols]

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


