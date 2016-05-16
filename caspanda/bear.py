###################################################
#################[ Module: Base ]##################
###################################################
"""
Class CasPanda, which subclasses cassandra.cluster.Cluster
and provides an interface between pandas and Cassandra.
"""
from cassandra.cluster import Cluster
from caspanda.metabear import ColumnMeta, KeyspaceMeta, TableMeta
from cassandra.query import dict_factory
from cassandra.cluster import _shutdown_cluster

from caspanda.bamboo import CassandraFrame

#TODO: Add describe function to name any keyspace or keyspace + table(s) to utilize MetaTable.describe function
class CasPanda(Cluster):
    """
    Interface for pandas and Cassandra.
    """
    keyspaces = None # contains all of the MetaKeyspaces info


    def __init__(self, *args, **kwargs):

        super(CasPanda, self).__init__(*args, **kwargs)
    def connect(self, kp=None):
        """
        Create `cassandra.cluster.Cluster` session, 
        and patch `session.row_factory` with `self.panda_factory`.

        :return: Session object
        """

        self.session = super(CasPanda, self).connect(kp)
        self.session.row_factory = self.panda_factory
        if self.keyspaces is None:
            self._sync_metadata(kp)

        return self.session

    def panda_factory(self, colnames, rows):
        """
        Returns Rows in a Panda DataFrame
        :param rows: values selected in Select statement
        :param colnames: column names selected
        :return: Panda DataFrame
        """
        if len(rows) == 0:
            return CassandraFrame(session=self.session)
        return CassandraFrame(rows, columns=colnames, session=self.session)

    def describe(self, kp=None, tb=None):

        pass

    def _sync_metadata(self, kp):
        """
        Syncs all of the metadata keyspaces and their underlying tables and columns. Sets keyspace to be a dict
        of all MetaKeyspace in the connection by name:MetaKeyspace
        :return:
        """

        self.keyspaces = {}
        #TODO: Turn off warnings when this occurs
        self.session.row_factory = dict_factory

        #gets all of the column data for all tables/keyspaces
        result = self.session.execute("""SELECT keyspace_name, columnfamily_name, column_name, component_index, index_name,
                             index_options, index_type, type as cql_type, validator FROM system.schema_columns""")


        cols = [ColumnMeta(**row) for row in result]
        for i in cols:
            #create keyspace if not already exists
            if self.keyspaces.get(i.keyspace) is None:
                self.keyspaces.update({i.keyspace:KeyspaceMeta(i.keyspace)})

            #add table if not already exists
            kp = self.keyspaces.get(i.keyspace)
            if kp.tables.get(i.table) is None:
                kp.tables.update({i.table:TableMeta(i.keyspace, i.table)})

            #finally add/overwrite column into table
            tb = kp.tables.get(i.table)
            tb.columns[i.name] = i
        for kp_nm, kp in self.keyspaces.iteritems():
            for tbl_nm, tbl in kp.tables.iteritems():
                tbl.categorize_columns()

        self.session.row_factory = self.panda_factory








