from cassandra.cluster import Cluster, Session
from cassandra.query import _clean_column_name
from pandas import DataFrame

class InputError(Exception):
    pass

class BaseCassandra(Cluster):
    def __init__(self, keyspace, *args, **kwargs):
        super(BaseCassandra, self).__init__()
        sn = kwargs.get("session") #allows you to pass and use the same session for objects connecting to cluster
        if sn is None:
            if keyspace is not None:
                self.keyspace = keyspace
            else:
                raise InputError("Specify Keyspace, keyspace='rts'")
            self.cluster = Cluster()
            self.session = self.cluster.connect(self.keyspace)
        else:
            assert isinstance(sn, Session)
            self.session = sn

class CassandraPanda(BaseCassandra):
    def __init__(self, keyspace, *args, **kwargs):
        super(CassandraPanda, self).__init__(keyspace, *args, **kwargs)
        self.session.row_factory = self.panda_factory

    def panda_factory(rows, colnames):
        """
        Returns Rows in a Panda DataFrame
        :param rows: values selected in Select statement
        :param colnames: column names selected
        :return: Panda DataFrame
        """

        cnames = _clean_column_name(colnames)

        return DataFrame(rows, columns=cnames)

