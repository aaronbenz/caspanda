###################################################
#################[ Script: Example ]################
###################################################
"""
Start a cassandra cluster and demonstrate inserting a CassandraFrame.
"""
import numpy as np
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.cluster import Session

from caspanda.bamboo import CassandraFrame
from caspanda.utils import paste


cl = Cluster()
session = cl.connect()

session.execute("""CREATE KEYSPACE IF NOT EXISTS tests WITH REPLICATION = { 'class' : 'SimpleStrategy',
                    'replication_factor' : 1 };""")
session.set_keyspace("tests")
session.execute("""CREATE TABLE IF NOT EXISTS albums(
                       id text PRIMARY KEY,
                       car text,
                       color text,
                       owner text,
                       passengers set<text>,
                       data blob
                    );""")

cols = ["id","car","color","owner"]

#df = pd.DataFrame(range(1,5), columns=["a"])
#tmp = CassandraFrame(np.random.randn(10, 2), columns=["id",""], session = session, table="albums")

tmp = CassandraFrame([["VIN1", "ford", "black", "frank"], ["VIN2", "cyrsler", "blue", "chris"], ["VIN3", "honda", "red", "harry"]],
                                  columns = cols, session=session, table="albums")
tmp.create_cql_insert()
print tmp.insert_async()

cl.shutdown()


#session.execute("DROP TABLE albums;")


