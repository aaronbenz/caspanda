from caspanda.base import CassandraPanda
from cassandra.cluster import Session
from pandas import DataFrame
import logging as log


class CassandraFrame(DataFrame):
    __prepared_columns = None
    statement_input = None
    __insert_index = None

    def __init__(self,  data=None, index=None, columns=None, cql = None, session=None, table=None, dtype=None,
                 copy=False, cql_columns=None, *args, **kwargs):
        super(CassandraFrame, self).__init__(data, index, columns, dtype, copy, *args, **kwargs)

        self.set_session(session)
        self.table = table
        self.cql = kwargs.get('cql', None)
        self.set_cql_columns(cql_columns)

    def put(self, table=None):
        if table is not None:
            self.table = table

        pass

    @property
    def create_cql_insert(self):
        """
        Given a table, prepares a statement to allow the dataframe to be inserted row by row into cassandra

        Sets statement_input to be the prepared statement
        :return: 0
        """
        assert isinstance(self.session, Session)
        assert self.table is not None

        statement = "INSERT INTO " + self.table + "(" + paste(self.cql_columns) + ") VALUES (" + paste(["?"] * len(self.columns)) + ");"
        self.statement_input = self.session.prepare(statement)
        self.__prepared_columns = self.cql_columns
        return 0

    def insert_sync(self):
        assert self.__cql_columns==self.__prepared_columns
        if self.statement_input is None:
            raise ValueError('statement_input not defined. Use create_cql_insert()')

        for index, row in self.loc[:,self.__prepared_columns].iterrows():
            self.session.execute(self.statement_input.bind(row))

        return 0

    def insert(self):
        assert self.cql_columns==self.__prepared_columns
        if self.statement_input is None:
            raise ValueError('statement_input not defined. Use create_cql_insert()')

        self.__insert_index = 0

        for i in range(min(120, self.__len__())):
            self.handle_success(None)

        return 0
    sentinel = object()

    # def insert_next(self, previous_result=sentinel):
        # if previous_result is not sentinel:
        #     if isinstance(previous_result, BaseException):
        #         log.error("Error on insert: %r", previous_result)
            # if num_finished.next() >= num_queries:
            #     finished_event.set()

        # if num_started.next() <= num_queries:
        #     future = session.execute_async(query)
            # NOTE: this callback also handles errors
            # future.add_callbacks(insert_next, insert_next)

    # for i in range(min(120, num_queries)):
    #     insert_next()

    # finished_event.wait()
    def handle_success(self, obj):
        assert self.__insert_index is not None

        if self.__insert_index < self.__len__():
            i = self.__unique_index__()
            future = self.session.execute_async(self.statement_input.bind(self.loc[i, self.__prepared_columns]))
            future.add_callback(self.handle_success, self.handle_error)

        return 0

    def __unique_index__(self):
        i = self.__insert_index
        self.__insert_index = i + 1
        return i

    def handle_error(self, exception):
        log.error("Failed to fetch data info: %s", exception)
        self.handle_success()
        return



    def get_cql_columns(self):
        return self.cql_columns

    def set_cql_columns(self, x=None):
        if x is None:
            self.cql_columns = self.columns.tolist()
        else:
            assert isinstance(x, list)
            self.cql_columns = x

        return 0

    def set_session(self, session):
        if session is None:
            self.session = None
        else:
            assert isinstance(session, Session)
            self.session = session
        return 0


def paste(x, sep = ", "):
    return str(x).strip("[]").replace("'","").replace(", ", sep)



