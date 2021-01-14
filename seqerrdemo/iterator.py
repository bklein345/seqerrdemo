from collections import Iterator


class PredicatedReadIterator(Iterator):
    """
    A PredicatedReadIterator iterates over reads in a AlignmentFile that
    pass a provided predicate.

    Reads are returned in the order in which they appear in the
    AlignmentFile.
    """
    def __init__(self, af, predicate):
        """
        Initializes an instance of class PredicatedReadIterator

        :param af: An AlignmentFile
        :param predicate: A predicate to apply to reads
        """
        self._stream = af.fetch()
        self._predicate = predicate

    def __next__(self):
        read = next(self._stream)
        while not self._predicate.apply(read):
            read = next(self._stream)
        return read

    def __iter__(self):
        return self


class PairedReadIterator(Iterator):
    """
    A PairedReadIterator accumulates read pairs from a provided iterator,
    and allows iteration over these read pairs.
    """
    def __init__(self, read_iterator):
        """
        Create a PairedReadIterator.
        :param read_iterator: the iterator to accumulate paired reads from
        """
        self._read_iterator = read_iterator
        self._pair_dictionary = dict()

    def __next__(self):
        read = next(self._read_iterator)
        query_name = read.query_name
        while query_name not in self._pair_dictionary:
            self._pair_dictionary[query_name] = read
            read = next(self._read_iterator)
            query_name = read.query_name

        other_read = self._pair_dictionary[query_name]
        del self._pair_dictionary[query_name]

        if read.is_read1:
            return read, other_read
        else:
            return other_read, read

    def __iter__(self):
        return self
