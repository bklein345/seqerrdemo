from unittest import TestCase

from seqerrdemo.writer import SequencingErrorWriter
from tests.utils import _MockOutput


class TestSequencingErrorWriter(TestCase):
    def setUp(self):
        self.output = _MockOutput()
        self.writer = SequencingErrorWriter(self.output)

    def test_not_writable(self):
        self.assertRaises(ValueError, SequencingErrorWriter, _MockOutput(False))

    def test_write(self):
        self.writer.write("query", [1, 2, 3])
        self.assertEqual("query\t1,2,3\n", self.output.output)
        self.writer.write("hello", [3, 12])
        self.assertEqual("query\t1,2,3\nhello\t3,12\n", self.output.output)
        self.writer.write("w", [3])
        self.assertEqual("query\t1,2,3\nhello\t3,12\nw\t3\n", self.output.output)
