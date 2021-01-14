from unittest import TestCase

from seqerrdemo.controller import SequencingErrorController
from seqerrdemo.predicate import MappingQualityPredicate
from tests.utils import _MockOutput, _FakeAlignmentFile, _make_test_read


class TestSequencingErrorController(TestCase):
    def setUp(self):
        self.output = _MockOutput()
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
        predicate = MappingQualityPredicate(20)
        self.controller = SequencingErrorController(af, predicate, self.output)

    def test_go(self):
        self.read5.query_sequence = "ACTAT"
        self.controller.go()
        self.assertEqual("3\t10,11,13\n", self.output.output)
