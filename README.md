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


Installation
------------
`$ python setup.py install`

should suffice to process dependencies for most users. 

You'll also need Cassandra:

`$ brew install cassandra`


Usage
-----
TODO: usage examples  


Tests
-----
There are some unit and integration tests in the `caspanda/tests/` directory.

Run from the command line with

`$ nosetests`


TODO
----  
* `$ grep -r TODO .`
* `create_cql_insert()` should return the string, and `insert_` methods should call it and execute the string







