#TODO delete keyspace after tests
#TODO Add tests for all possibilities: table, [table], keyspace, [keyspace]
"""
Testing the describe functions and those in spots.py
"""
import unittest

from caspanda.bear import CasPanda
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

class TestQuery(BaseTestInput):

    def setUp(self):
        super(TestQuery, self).setUp()
        schema_columns={}

    def test_single_table(self):
        pass
