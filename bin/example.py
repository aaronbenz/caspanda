from caspanda.bamboo import CassandraFrame, paste
from pandas import DataFrame
from cassandra.cluster import Cluster, Session
import numpy as np
cl = Cluster()
session = cl.connect()

session.execute("""CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy',
                    'replication_factor' : 1 };""")
session.set_keyspace("test")
session.execute("""CREATE TABLE IF NOT EXISTS albums(
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

tmp = CassandraFrame([["VIN1", "ford", "black", "frank"], ["VIN2", "cyrsler", "blue", "chris"], ["VIN3", "honda", "red", "harry"]],
                                  columns = cols, session=session, table="albums")

tmp.create_cql_insert
tmp.insert()


#session.execute("DROP TABLE albums;")


