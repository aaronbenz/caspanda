###################################################
#################[ Module: Base ]##################
###################################################
"""
Class CasPanda, which subclasses cassandra.cluster.Cluster
and provides an interface between pandas and Cassandra.
"""
from cassandra.cluster import Cluster
from cassandra.cluster import _shutdown_cluster

from caspanda.bamboo import CassandraFrame


class CasPanda(Cluster):
    """
    Interface for pandas and Cassandra.
    """
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
        return self.session

    def panda_factory(self, colnames, rows):
        """
        Returns Rows in a Panda DataFrame
        :param rows: values selected in Select statement
        :param colnames: column names selected
        :return: Panda DataFrame
        """
        return CassandraFrame(rows, columns=colnames, session=self.session)

    def describe(self, kp=None, tb=None):

        pass




