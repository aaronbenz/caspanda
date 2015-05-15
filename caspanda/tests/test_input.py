import unittest

from caspanda.base import CassandraPanda
from caspanda.bamboo import CassandraFrame

cl = CassandraPanda()
session = cl.connect()

session.execute("""CREATE KEYSPACE IF NOT EXISTS tests WITH REPLICATION = { 'class' : 'SimpleStrategy',
                    'replication_factor' : 1 };""")
session.set_keyspace("tests")
session.execute("""CREATE TABLE IF NOT EXISTS tester(
                       id text PRIMARY KEY,
                       car text,
                       color text,
                       owner text,
                       passengers set<text>,
                       data blob
                    );""")

cols = ["id","car","color","owner"]
#df = DataFrame(range(1,5), columns=["a"])
#tmp = CassandraFrame(np.random.randn(10, 2), columns=["id",""], session = session, table="albums")

class query(unittest.TestCase):
    def setUp(self):
        self.tmp = CassandraFrame([["VIN1", "ford", "black", "frank"],
                              ["VIN2", "cyrsler", "blue", "chris"],
                              ["VIN3", "honda", "red", "harry"]],
                                  columns = cols, session=session, table="tester")
        self.tmp.create_cql_insert


    def test_all_attributes(self):
        self.tmp.insert_async()
        self.cf = session.execute("SELECT * FROM tester")

        self.assertEqual(len(self.cf), 3)
        self.assertIsInstance(self.cf, CassandraFrame)
        self.assertEqual(self.tmp.session, self.cf.session)
#        self.assertEqual(self.tmp.table, self.cf.table)
#        self.assertEqual(self.tmp.__prepared_columns__, self.cf.__prepared_columns__)
#        self.assertEqual(self.tmp.cql_columns, self.cf.cql_columns)