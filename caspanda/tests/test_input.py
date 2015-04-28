import unittest
from caspanda.base import CassandraPanda

K = "rts"

class TestReturnKey(unittest.TestCase):
    def setUp(self):
        self.rts = CassandraPanda(keyspace=K)
        super(TestReturnKey,self).setUp()
        self.pk = ["this is a pk"]
        self.uid = self.rts.return_key(self.pk)

    def test_return_key_uid(self):
        self.assertEqual(self.uid, self.rts.return_key(["thisiSApk"]))
        self.assertEqual(self.uid, self.rts.return_key(["THIS IsA Pk"]))