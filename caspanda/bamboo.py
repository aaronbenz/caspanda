from caspanda.base import CassandraPanda
from cassandra.cluster import Session
from pandas import DataFrame

class CassandraFrame(DataFrame):
    __prepared_columns = None
    statement_input = None
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

        Sets statement_input to be the prepared statemetn
        :return: 0
        """
        assert isinstance(self.session, Session)
        assert self.table is not None

        statement = "INSERT INTO " + self.table + "(" + paste(self.__cql_columns) + ") VALUES (" + paste(["?"] * len(self.columns)) + ");"
        self.statement_input = self.session.prepare(statement)
        self.__prepared_columns = self.__cql_columns
        return 0

    def insert(self):
        assert self.__cql_columns==self.__prepared_columns
        if self.statement_input is None:
            raise ValueError('statement_input not defined. Use create_cql_insert()')
        result = []
        for index, row in self.loc[:,self.__prepared_columns].iterrows():
            result.append(self.session.execute(self.statement_input.bind(row)))

        return result

    def get_cql_columns(self):
        return self.___get_cql_columns

    def set_cql_columns(self, x=None):
        if x is None:
            self.__cql_columns = self.columns.tolist()
        else:
            assert isinstance(x, list)
            self.__cql_columns = x

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



