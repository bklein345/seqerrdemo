from unittest import TestCase


from seqerrdemo.predicate import MappingQualityPredicate, OverlappingReadPairPredicate, UnionPredicate
from tests.utils import _make_test_read


class TestMappingQualityPredicate(TestCase):
    def setUp(self):
        self.predicate = MappingQualityPredicate(20)

    def test_threshold_too_low(self):
        self.assertRaises(ValueError, MappingQualityPredicate, -1)

    def test_threshold(self):
        self.assertEqual(20, self.predicate.threshold)

    def test_apply(self):
        read = _make_test_read(mapping_quality=19)
        self.assertFalse(self.predicate.apply(read))
        read = _make_test_read(mapping_quality=20)
        self.assertTrue(self.predicate.apply(read))
        read = _make_test_read(mapping_quality=21)
        self.assertTrue(self.predicate.apply(read))


class TestOverlappingReadPairPredicate(TestCase):
    def setUp(self):
        self.predicate = OverlappingReadPairPredicate()

    def test_apply(self):
        read = _make_test_read(template_length=10, query_length=10,
                               is_proper_pair=False)
        self.assertFalse(self.predicate.apply(read))
        read = _make_test_read(template_length=10, query_length=5,
                               is_proper_pair=True)
        self.assertFalse(self.predicate.apply(read))
        read = _make_test_read(template_length=11, query_length=6,
                               is_proper_pair=True)
        self.assertTrue(self.predicate.apply(read))


class TestUnionPredicate(TestCase):
    def setUp(self):
        self.mapping_predicate = MappingQualityPredicate(20)
        self.overlap_predicate = OverlappingReadPairPredicate()
        self.union_predicate = UnionPredicate()

    def test_predicates(self):
        self.assertEqual(set(), self.union_predicate.predicates)

    def test_add(self):
        self.union_predicate.add(self.mapping_predicate)
        self.assertEqual({self.mapping_predicate}, self.union_predicate.predicates)
        self.union_predicate.add(self.overlap_predicate)
        self.assertEqual({self.mapping_predicate, self.overlap_predicate}, self.union_predicate.predicates)

    def test_apply(self):
        read = _make_test_read(mapping_quality=15, template_length=10,
                               query_length=5, is_proper_pair=False)
        self.assertTrue(self.union_predicate.apply(read))
        self.union_predicate.add(self.mapping_predicate)
        self.assertFalse(self.union_predicate.apply(read))
        read = _make_test_read(mapping_quality=20, template_length=10,
                               query_length=5, is_proper_pair=False)
        self.assertTrue(self.union_predicate.apply(read))
        self.union_predicate.add(self.overlap_predicate)
        self.assertFalse(self.union_predicate.apply(read))
        read = _make_test_read(mapping_quality=20, template_length=10,
                               query_length=6, is_proper_pair=True)
        self.assertTrue(self.union_predicate.apply(read))
