from unittest import TestCase

from seqerrdemo.iterator import PredicatedReadIterator, PairedReadIterator
from seqerrdemo.predicate import MappingQualityPredicate
from tests.utils import _FakeAlignmentFile, _make_test_read


class TestPredicatedReadIterator(TestCase):
    def setUp(self):
        predicate = MappingQualityPredicate(20)
        af = _FakeAlignmentFile()
        self.read1 = _make_test_read(mapping_quality=20)
        self.read2 = _make_test_read(mapping_quality=19)
        self.read3 = _make_test_read(mapping_quality=21)
        af.add_read(self.read1)
        af.add_read(self.read2)
        af.add_read(self.read3)
        self.iterator = PredicatedReadIterator(af, predicate)

    def test_next(self):
        self.assertEqual(self.read1, next(self.iterator))
        self.assertEqual(self.read3, next(self.iterator))

    def test_iter(self):
        self.assertEqual([self.read1, self.read3], [x for x in self.iterator])


class TestPairedReadIterator(TestCase):
    def setUp(self):
        predicate = MappingQualityPredicate(20)
        af = _FakeAlignmentFile()
        self.read1 = _make_test_read(query_name="1", mapping_quality=20, is_read1=True)
        self.read2 = _make_test_read(query_name="1", mapping_quality=20, is_read1=False)
        self.read3 = _make_test_read(query_name="2", mapping_quality=19, is_read1=True)
        self.read4 = _make_test_read(query_name="2", mapping_quality=19, is_read1=False)
        self.read5 = _make_test_read(query_name="3", mapping_quality=21, is_read1=True)
        self.read6 = _make_test_read(query_name="3", mapping_quality=21, is_read1=False)
        af.add_read(self.read1)
        af.add_read(self.read2)
        af.add_read(self.read3)
        af.add_read(self.read4)
        af.add_read(self.read5)
        af.add_read(self.read6)
        self.iterator = PairedReadIterator(PredicatedReadIterator(af, predicate))

    def test_next(self):
        self.assertEqual((self.read1, self.read2), next(self.iterator))
        self.assertEqual((self.read5, self.read6), next(self.iterator))

    def test_iter(self):
        self.assertEqual([(self.read1, self.read2), (self.read5, self.read6)],
                         [x for x in self.iterator])
