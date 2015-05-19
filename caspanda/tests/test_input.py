###################################################
#################[ Module: Test Input ]############
###################################################
"""
Test inserting CassandraFrame into Cassandra and ensure database get returns expected output.
"""
import unittest

from caspanda.base import CassandraPanda
from caspanda.bamboo import CassandraFrame


class BaseTestInput(unittest.TestCase):
    """
    Base class for input testing.

    Connects to database.
    """  
    def __init__(self):
        self.cl = CassandraPanda()
        self.session = self.cl.connect()
        self.session.execute("""CREATE KEYSPACE IF NOT EXISTS tests WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 };""")
        self.session.set_keyspace("tests")
        self.session.execute("""CREATE TABLE IF NOT EXISTS tester(
                                    id text PRIMARY KEY,
                                    car text,
                                    color text,
                                    owner text,
                                    passengers set<text>,
                                    data blob
                                );""")

        self.cols = ["id","car","color","owner"]


class TestQuery(BaseTestInput):

    def setUp(self):
        self.frame = CassandraFrame([["VIN1", "ford", "black", "frank"],
                                     ["VIN2", "cyrsler", "blue", "chris"],
                                     ["VIN3", "honda", "red", "harry"]],
                                    columns=self.cols, session=self.session, table="tester")

        self.frame.create_cql_insert()


    def test_all_attributes(self):
        self.frame.insert_async()
        self.cf = session.execute("SELECT * FROM tester")

        self.assertEqual(len(self.cf), 3)
        self.assertIsInstance(self.cf, CassandraFrame)
        self.assertEqual(self.tmp.session, self.cf.session)








