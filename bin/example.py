###################################################
#################[ Script: Example ]################
###################################################
"""
Start a cassandra cluster and demonstrate inserting a CassandraFrame.
"""
from caspanda.bear import CasPanda
from caspanda.bamboo import CassandraFrame


cl = CasPanda()
session = cl.connect()

session.execute("""CREATE TABLE IF NOT EXISTS tests.sold_cars (
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

session = cl.connect("tests")

#df = pd.DataFrame(range(1,5), columns=["a"])
#tmp = CassandraFrame(np.random.randn(10, 2), columns=["id",""], session = session, table="albums")

tmp = CassandraFrame([["VIN1", "ford", "black", "frank"], ["VIN2", "cyrsler", "blue", "chris"], ["VIN3", "honda", "red", "harry"]],
                     columns=cols, session=session, table="albums")

tmp.create_cql_insert()
tmp.insert_async()

print "Now see that the data was inserted"
session.execute("""SELECT id, car, color, owner FROM tests.albums""")

print "The description of tests.albumns:"
print cl.keyspaces["tests"].tables["albums"].describe()
print "As opposed to this:"
print cl.metadata.keyspaces["tests"].tables["albums"].export_as_string()

print "-----------------------------------------"
print "Another comparison"
print cl.keyspaces["system"].tables["schema_columns"].describe()
print "As opposed to this:"
print cl.metadata.keyspaces["system"].tables["schema_columns"].export_as_string()
print "-----------------------------------------"


print "Another comparison"
print cl.keyspaces["tests"].tables["sold_cars"].describe()
print "As opposed to this:"
print cl.metadata.keyspaces["tests"].tables["sold_cars"].export_as_string()




cl.shutdown()




#session.execute("DROP TABLE albums;")


