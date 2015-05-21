#TODO delete keyspace after tests
#TODO Add tests for all possibilities: table, [table], keyspace, [keyspace]
"""
Testing the describe functions and those in spots.py
"""
import unittest

from caspanda.bear import CasPanda
from caspanda.bamboo import CassandraFrame

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

