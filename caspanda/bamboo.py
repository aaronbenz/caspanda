###################################################
#################[ Module: Bamboo ]################
###################################################
"""
This module contains the CassandraFrame class, which exposes the main interface between pandas and Cassandra.

Bamboo, like what PANDAS eat. Get it??

CassandraFrame implements synchronous and asynchronous insertion operations, and MultiIndexes output from Cassandra
in order to support pivot- and melt-like operations.
"""
import logging
import pandas as pd
from Queue import Queue
from Queue import Empty
from cassandra.cluster import Session

from caspanda.utils import paste


class CassandraFrame(pd.DataFrame):
    """
    Wrapper for pandas.DataFrame.

    Implements convenience methods for get and put operations to Cassandra,
    and handles MultiIndexing of CQL output.

    Keeps track of column name hierarchy in the self._prepared_columns and self._cql_columns.
    """
    statement_input      = None
    _prepared_columns    = None
    _insert_index        = None


    def __init__(self, data=None, index=None, columns=None, cql=None, session=None, table=None, dtype=None,
                 copy=False, cql_columns=None, *args, **kwargs):

        super(CassandraFrame, self).__init__(data, index=index, columns=columns, dtype=dtype, copy=copy, *args, **kwargs)

        self.set_session(session)

        self.table         = table
        self.cql           = kwargs.get('cql', None)
        self.insert_queue  = Queue()
 
        self.set_cql_columns(cql_columns)


    def put(self, table=None):
        """
        TODO: (???)
        """
        if table is not None:
            self.table = table
        pass


    def create_cql_insert(self):
        """
        Given a table, prepares a statement to allow the dataframe to be inserted row by row into cassandra.

        Sets statement_input to be the prepared statement.

        :return: 0
        """
        assert isinstance(self.session, Session)
        assert self.table is not None

        statement = "INSERT INTO " + self.table + "(" + paste(self._cql_columns) + ") VALUES (" + paste(["?"] * len(self.columns)) + ");"

        self.statement_input   = self.session.prepare(statement)
        self._prepared_columns = self._cql_columns

        return


    def insert_sync(self):
        """
        Insert rows synchronously into Cassandra.

        Cassandra doesn't get a performance improvement from batch insertion as it is a peer-to-peer architecture;
        so the insertion strategy is to iterate over the CassandraFrame's rows and bind them one by one.
        """
        assert self._cql_columns == self._prepared_columns
        assert self.statement_input is not None, 'Statement_input not defined. Use create_cql_insert().'

        for index, row in self.loc[:,self._prepared_columns].iterrows():
            self.session.execute(self.statement_input.bind(row))

        return


    def insert_async(self):
        """
        Insert rows asynchronously into Cassandra.

        TODO: distinguish from the chained callback approach in insert_callback() and clean up.
        """
        assert self._cql_columns == self._prepared_columns
        assert self.statement_input is not None, 'Statement_input not defined. Use create_cql_insert().'

        def handle_success(rows):
            pass

        def handle_error(exception):
            logging.error("Failed to send data info: %s", exception)
            return

        def put(i):
            future = self.session.execute_async(self.statement_input.bind(self.loc[i, self._prepared_columns]))
            future.add_callbacks(handle_success, handle_error)
            return future

        map(put, range(self.__len__()))

        return


    def insert_callback(self):
        """
        TODO: code the upper limit on concurrent futures, clean up (and deprecate insert_async??)

        Put row indices into a queue; 
        while the queue is not empty and the upper threshold on number of concurrent waiting processes is not reached,
        insert a new row into Cassandra.
        """
        assert self._cql_columns == self._prepared_columns
        assert self.statement_input is not None, 'Statement_input not defined. Use create_cql_insert().'

        map(self.insert_queue.put_nowait, range(self.__len__()))

        def handle_success(rows):
            """
            Queue raises an Empty exception when it hits the bottom of the queue (after blocking for `timeout` seconds).

            Try getting until Queue is exhausted, then return.
            """
            try:
                i = self.insert_queue.get()
            except Empty:
                return

            print "Inserting", self.iloc[i].name, " ..." 
            print "-----------------------------------------------"

            future = self.session.execute_async(self.statement_input.bind(self.loc[i, self._prepared_columns]))

            future.add_callbacks(handle_success, handle_error)  # intentional tail recursion!
                                                                # need hard upper limit on number of concurrent futures
                                                                # something like: for i in range(min(120, self.__len__())):
            return future

        def handle_error(exception):
            """
            Log error and recurse.
            """
            logging.error("Failed to send data info: %s", exception)
            future = handle_success(None)
            return future

        future = handle_success(None)

        return future.result()


    def get_cql_columns(self):
        return self._cql_columns


    def set_cql_columns(self, x=None):
        if x is None:
            self._cql_columns = self.columns.tolist()
        else:
            assert isinstance(x, list)
            self._cql_columns = x

        return


    def set_session(self, session):
        """
        Setter method for self.session.

        Pass a session object or None.

        :return: None
        """
        if session is None:
            self.session = None

        else:
            assert isinstance(session, Session), "Got non-session, type: {}".format(type(session))
            self.session = session

        return



