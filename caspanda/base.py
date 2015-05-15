from cassandra.cluster import Cluster, _shutdown_cluster
from caspanda.bamboo import CassandraFrame

class InputError(Exception):
    pass

class CassandraPanda(Cluster):
    def __init__(self, *args, **kwargs):
        super(CassandraPanda, self).__init__(*args, **kwargs)


    def connect(self, keyspace=None):
       self.session = super(CassandraPanda, self).connect(keyspace)
       self.session.row_factory = self.panda_factory
       return self.session


    def panda_factory(self, colnames, rows):
        """
        Returns Rows in a Panda DataFrame
        :param rows: values selected in Select statement
        :param colnames: column names selected
        :return: Panda DataFrame
        """
        return CassandraFrame(rows, columns=colnames, session=self.session)

