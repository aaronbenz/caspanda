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

Caspanda Pretty Print/Description of that table:

```python

print cl.keyspaces["tests"].tables["albums"].describe()

#make, state
#		day
#			event_time
#				dealership
#				year
#				salesman
#		distributor_lead
#		account_lead
```

As opposed to this:

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
#) WITH CLUSTERING ORDER BY (day ASC, event_time ASC)
#    AND bloom_filter_fp_chance = 0.01
#    AND caching = '{"keys":"ALL", "rows_per_partition":"NONE"}'
#    AND comment = ''
#    AND compaction = {'min_threshold': '4', 'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32'}
#    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.LZ4Compressor'}
#    AND dclocal_read_repair_chance = 0.1
#    AND default_time_to_live = 0
#    AND gc_grace_seconds = 864000
#    AND max_index_interval = 2048
#    AND memtable_flush_period_in_ms = 0
#    AND min_index_interval = 128
#    AND read_repair_chance = 0.0
#    AND speculative_retry = '99.0PERCENTILE';
```

Installation
----
`$ python setup.py install`

should suffice to process dependencies for most users. 

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
* brainstorm naming convention for CassandraPanda--  
  not really clear what it's for / why it's needed from the name  
* 









