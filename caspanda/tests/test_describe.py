#TODO delete keyspace after tests
#TODO Add tests for all possibilities: table, [table], keyspace, [keyspace]
"""
Testing the describe functions and those in spots.py
"""
import unittest

from caspanda.bear import CasPanda
from caspanda.metabear import KeyspaceMeta, TableMeta, ColumnMeta
from caspanda.spots import describe

class BaseTestInput(unittest.TestCase):
    """
    Base class for input testing.

    Connects to database.
    """
    def setUp(self):
        self.cl = CasPanda()
        self.cl.connect()
        super(BaseTestInput, self).setUp()
        cl = CasPanda()
        session = cl.connect()
        session.execute("""CREATE KEYSPACE IF NOT EXISTS tests WITH REPLICATION = { 'class' : 'SimpleStrategy',
                            'replication_factor' : 1 };""")
        session.set_keyspace("tests")
        session.execute("""CREATE TABLE IF NOT EXISTS sold_cars (
            make text,
            state text,
            day timestamp,
            event_time timestamp,
            dealership text,
            salesman text,
            year int,
            account_lead text static,
            distributor_lead text static,
            PRIMARY KEY ((make, state), day, event_time));""")

#class TestDescribe(BaseTestInput):

    # def setUp(self):
    #     super(TestDescribe, self).setUp()
    #
    # def test_single_table(self):
    #     out = "make, state\n\t\tday\n\t\t\tevent_time\n\t\t\t\tdealership\n\t\t\t\tyear\n\t\t\t\tsalesman\n\t\tdistributor_lead\n\t\taccount_lead\n"
    #     self.assertEqual(out, self.cl.keyspaces["tests"].tables["sold_cars"])

class TestColumnStructure(BaseTestInput):
    def setUp(self):
        super(TestColumnStructure, self).setUp()
        schema_columns={}

    def test_single_table(self):

        self.assertIsInstance(self.cl.keyspaces, dict)
        self.assertIsInstance(self.cl.keyspaces["tests"], KeyspaceMeta)
        self.assertIsInstance(self.cl.keyspaces["tests"].tables, dict)

        tb = self.cl.keyspaces["tests"].tables["sold_cars"]

        self.assertIsInstance(tb, TableMeta)
        self.assertEqual(len(tb.columns), 9)
        self.assertIsInstance(tb.columns, dict)
        self.assertIsInstance(tb.columns["account_lead"], ColumnMeta)

        self.assertEqual(tb.columns["account_lead"].cql_type, "static")

    def test_columns(self):
        tb = self.cl.keyspaces["tests"].tables["sold_cars"]
        col_day = tb.columns["day"]
        self.assertEqual(col_day.cql_type, "clustering_key")
        self.assertEqual(col_day.component_index, 0)
        self.assertEqual(col_day.keyspace, "tests")
        self.assertEqual(col_day.name, "day")
        self.assertEqual(col_day.table, "sold_cars")

        col_state = tb.columns["state"]
        self.assertEqual(col_state.cql_type, "partition_key")
        self.assertEqual(col_state.component_index, 1)
        self.assertEqual(col_state.keyspace, "tests")
        self.assertEqual(col_state.name, "state")
        self.assertEqual(col_state.table, "sold_cars")

        col_state = tb.columns["salesman"]
        self.assertEqual(col_state.cql_type, "regular")
        self.assertEqual(col_state.component_index, 2)
        self.assertEqual(col_state.keyspace, "tests")
        self.assertEqual(col_state.name, "salesman")
        self.assertEqual(col_state.table, "sold_cars")


        col_state = tb.columns["account_lead"]
        self.assertEqual(col_state.cql_type, "static")
        self.assertEqual(col_state.component_index, 2)
        self.assertEqual(col_state.keyspace, "tests")
        self.assertEqual(col_state.name, "account_lead")
        self.assertEqual(col_state.table, "sold_cars")

