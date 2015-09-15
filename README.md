[![Build Status](https://travis-ci.org/aaronbenz/caspanda.svg?branch=master)](https://travis-ci.org/aaronbenz/caspanda)
[![codecov.io](http://codecov.io/github/aaronbenz/caspanda/coverage.svg?branch=master)](http://codecov.io/github/aaronbenz/caspanda?branch=master)
```
                                     _       
  ___ __ _ ___ _ __   __ _ _ __   __| | __ _ 
 / __/ _` / __| '_ \ / _` | '_ \ / _` |/ _` |
| (_| (_| \__ \ |_) | (_| | | | | (_| | (_| |
 \___\__,_|___/ .__/ \__,_|_| |_|\__,_|\__,_|
              |_|                            

Aaron Benz
Charlie Hack
Spring 2015
```

caspanda
========
Pandas interface for Cassandra.

##What is it?
**caspanda** is a Python module combines **Apache Cassandra** with **Python's Pandas** module... aka **caspanda**. Its
overall goal is to give the user the ability to seperate Cassandra's NoSQL backend from the user's front end experience.
Ultimately, it hopes to provide Data Scientists who use Pandas the ability to easily use Cassandra.

It is still very early in its developement, but it plans on using the multi-indexing/pivot ability and the time series
functionality available in Pandas to automatically sort and organize a data coming from Cassandra according to its schema.
Additionally, it hopes to allow the user to easily insert data back into cassandra without ever having to speak CQL.

Main Features
----
Here are a few of the things caspanda currently does:

    - Puts queried data into a Pandas Dataframe
    - Stores data into Cassandra using CassandraFrames (uses sync and async methods)
    - Describes the structure of Cassandra Tables in a hierarchical way

Usage
----
One of the main objectives of **Caspandas** is being able to easily understand and use Cassandra. Unfortunately,
 many can be misled or lack the understanding of how Cassandra actually stores it's data. The attempt below is meant to 
 give you a conceptual understanding of the hierarchy that the data is really stored in.  
 
 The example table `sold_cars` demonstrates a data model that might exist if you wanted to store the information about
 sold cars. It stores information about a sale according to the *make* and *state* of the car, and then 
 stores the information by day and time. So, the query pattern would specify the *make* and *state*, and then give you 
 the ability to choose a date range. 
 
 Conceptually this might make since, but the way in which it is written down in CQL if often difficult to grasp for anyone
 not seasoned in Cassandra. So, we have tried to make this much more simple. First, connect to Cassandra and create the
 table `sold_cars`
```python
from caspanda.bear import CasPanda

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
```

Now that the table has been created, let's visualize it. This breaks down the names of the columns in a hierarchical
fashion that demonstrates how it is actually stored. So for example, The *make* and *state* columns define a group of data.
That group is ordered and stored by *day*, and then by *event_time*. Then, for each *event_time*,
there are fields for a *dealership*, *year*, and *salesman*. Additionally, there is a single value column stored on the
same level as *day*, which is *distributor* and *account_lead*. 

Said differently, for every *make* and *state*, there is one *distributor_lead* and one *account_lead*. Also, for every
*make* and *state*, there can be a combination of *dealership*, *year*, and *salesman* defined by (indexed by) a *day*
and then by an *event_time*

```python

print cl.keyspaces["tests"].tables["albums"]

#	make text partition_key
#	state text partition_key
#		day timestamp clustering_key
#			event_time timestamp clustering_key
#				dealership text 
#				year int 
#				salesman text 
#		distributor_lead text static
#		account_lead text static
```

The traditional method for viewing this in CQL is this:

```python

print cl.metadata.keyspaces["tests"].tables["sold_cars"].export_as_string()

#CREATE TABLE tests.sold_cars (
#    make text,
#    state text,
#    day timestamp,
#    event_time timestamp,
#    account_lead text static,
#    dealership text,
#    distributor_lead text static,
#    salesman text,
#    year int,
#    PRIMARY KEY ((make, state), day, event_time)
```

With that being said, please feel free to reach out to us for comments/suggestions/questions. 

There are also some more examples for calling data from Cassandra and inserting it back using only a Pandas Dataframe (which
we called a CassandraFrame), in `bin/example.py`

Selecting data
----
Running a Select from a Cassandra table will automatically return a Pandas Dataframe
Let's say you have a keyspace called 'tr_data' and you create one table 'tr_minute' with the following columns:

```
cqlsh:tr_data> create table tr_minute (
 ccypair text,
 gmt_timestamp timestamp,
 mid_rate double,
 ric text static,
 PRIMARY KEY (ccypair, gmt_timestamp) );
```
If the Cassandra database is running on localhost, you can connect using connect() as usual, then switch to the 'tr_data' keyspace. Any keywords controlling the connection such as the port or using compression are added as arguments to the initial CasPanda() call.
```python
from caspanda.bear import CasPanda
cl = CasPanda(compression=True)
cpsession = cl.connect()
cpsession.set_keyspace('tr_data')
select_ccys_distinct = """select distinct ccypair from tr_minute"""
ccys = cpsession.execute(select_ccys_distinct)
ccys.head()
```


Installation
----
`$ python setup.py install` or `$ pip install -e .`
You'll also need Cassandra:

`$ brew install cassandra`



Tests
-----
There are some unit and integration tests in the `caspanda/tests/` directory.

Run from the command line with

`$ nosetests`


TODO
----  
* `grep -r TODO .`









