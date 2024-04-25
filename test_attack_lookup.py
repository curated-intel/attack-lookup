import unittest

from attack_lookup.mapping import AttackMapping

class AttackLookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = AttackMapping()
        if not cls.mapping.load_data():
            raise Exception("failed to load att&ck data")

    def test_single_id(self):
        self.assertEqual("Hijack Execution Flow", self.mapping.lookup("T1574"))
        self.assertEqual("Hijack Execution Flow", self.mapping.lookup("t1574"))
        
        self.assertEqual("Resource Development", self.mapping.lookup("TA0042"))
        self.assertEqual("Resource Development", self.mapping.lookup("tA0042"))
    
    def test_multiple_results(self):
        self.assertEqual("Multiple possible values: T1583.001, T1584.001", self.mapping.lookup("Domains"))

    def test_nothing(self):
        self.assertTrue("No value found for" in self.mapping.lookup("nonexistent technique asdf"))

class AttackOfflineLookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = AttackMapping(offline=True)
        if not cls.mapping.load_data():
            raise Exception("failed to load att&ck data")

    def test_single_id(self):
        self.assertEqual("Hijack Execution Flow", self.mapping.lookup("T1574"))
        self.assertEqual("Hijack Execution Flow", self.mapping.lookup("t1574"))
        
        self.assertEqual("Resource Development", self.mapping.lookup("TA0042"))
        self.assertEqual("Resource Development", self.mapping.lookup("tA0042"))
    
    def test_multiple_results(self):
        self.assertEqual("Multiple possible values: T1583.001, T1584.001", self.mapping.lookup("Domains"))

    def test_nothing(self):
        self.assertTrue("No value found for" in self.mapping.lookup("nonexistent technique asdf"))