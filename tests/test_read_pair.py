from unittest import TestCase

from seqerrdemo.read_pair import ReadPair
from tests.utils import _make_test_read


class TestReadPair(TestCase):
    def setUp(self):
        self.read1 = _make_test_read(is_read1=True)
        self.read2 = _make_test_read(is_read1=False)
        self.read_pair = ReadPair(self.read1, self.read2)

    def test_query_names_dont_match(self):
        self.read1.query_name = "blah"
        self.assertRaises(ValueError, ReadPair, self.read1, self.read2)

    def test_not_read1(self):
        self.read1.is_read1 = False
        self.assertRaises(ValueError, ReadPair, self.read1, self.read2)

    def test_not_read2(self):
        self.read2.is_read1 = True
        self.assertRaises(ValueError, ReadPair, self.read1, self.read2)

    def test_read1(self):
        self.assertEqual(self.read1, self.read_pair.read1)

    def test_read2(self):
        self.assertEqual(self.read2, self.read_pair.read2)

    def test_query_name(self):
        self.assertEqual("query", self.read_pair.query_name)

    def test_get_sequencing_errors(self):
        self.read1.reference_start = 10
        self.read2.reference_start = 30
        self.read2.query_sequence = "AACTA"
        self.assertEqual(list(), self.read_pair.get_sequencing_errors())

        self.read2.reference_start = 10
        self.assertEqual([12, 13], self.read_pair.get_sequencing_errors())

        self.read2.query_sequence = "TTTTT"
        self.assertEqual([10, 11, 12, 13, 14], self.read_pair.get_sequencing_errors())

        self.read2.query_sequence = "AAAAA"
        self.assertEqual(list(), self.read_pair.get_sequencing_errors())
