from abc import ABC, abstractmethod


class ReadPredicate(ABC):
    """
    A ReadPredicate represents a tests for a read.
    """
    @abstractmethod
    def apply(self, read):
        """
        Determine if the provided read passes this predicate.

        :param read: an AlignedSegment
        :return: true if the read passes the predicate, false otherwise
        """
        pass


class MappingQualityPredicate(ReadPredicate):
    """
    A MappingQualityPredicate tests whether a read has above or equal to
    a provided mapping quality threshold.
    """
    def __init__(self, threshold):
        """
        Create a MappingQualityPredicate.

        :param threshold: the mapping quality threshold.
        :raises ValueError: if threshold is less than zero
        """
        if threshold < 0:
            raise ValueError("threshold must be >= zero")
        self._threshold = threshold

    @property
    def threshold(self):
        """The mapping quality threshold"""
        return self._threshold

    def apply(self, read):
        return read.mapping_quality >= self.threshold


class OverlappingReadPairPredicate(ReadPredicate):
    """
    An OverlappingReadPairPredicate tests whether a read is properly
    paired and is likely to overlap its mate pair.

    Passing this predicate does not guarantee that a read overlaps its
    mate.
    """
    def apply(self, read):
        return read.is_proper_pair and read.template_length < 2*read.query_length


class UnionPredicate(ReadPredicate):
    """
    A UnionPredicate tests whether a read passes all of its member
    predicates.
    """
    def __init__(self):
        """Create a UnionPredicate"""
        self._predicates = set()

    @property
    def predicates(self):
        """The predicates in this union"""
        return self._predicates

    def add(self, predicate):
        """
        Add a predicate to this union.

        :param predicate: the predicate to add.
        """
        self._predicates.add(predicate)

    def apply(self, read):
        for predicate in self._predicates:
            if not predicate.apply(read):
                return False
        return True
