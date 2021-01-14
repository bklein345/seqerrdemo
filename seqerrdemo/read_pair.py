def _get_position_base_map(read):
    """
    Get a map from position to called base for a given read.

    :param read: An AlignedSegment
    :return: a map from sequenced positions to called base
    """
    position_base_map = dict()
    for aligned_pair in read.get_aligned_pairs():
        query_index = aligned_pair[0]
        position = aligned_pair[1]

        if query_index is None or position is None:
            continue

        base = read.query_sequence[query_index]
        position_base_map[position] = base

    return position_base_map


class ReadPair(object):
    """
    A ReadPair represents a set of paired next-generation sequencing reads.
    """

    def __init__(self, read1, read2):
        """
        Create a ReadPair.

        :param read1: The first read of the pair
        :param read2: The second read of the pair
        :raises ValueError: if read1 and read2 do not have the same query name
        :raises ValueError: if read1 is not read1, or read2 is read1
        """
        if read1.query_name != read2.query_name:
            raise ValueError("reads must have the same query name")
        if not read1.is_read1:
            raise ValueError("read1 must be read1")
        if read2.is_read1:
            raise ValueError("read2 should not be read1")
        self._read1 = read1
        self._read2 = read2

    @property
    def read1(self):
        """The first read in this pair"""
        return self._read1

    @property
    def read2(self):
        """The second read in this pair"""
        return self._read2

    @property
    def query_name(self):
        """The query name of this read pair"""
        return self.read1.query_name

    def get_sequencing_errors(self):
        """
        Get the positions of sequencing errors observed on these paired reads.

        Note that this only returns the positions of substitution errors.
        Insertion and deletion errors are ignored.

        :return: A list of positions where these reads disagree on their
        called base.
        """
        read1_map = _get_position_base_map(self.read1)
        read2_map = _get_position_base_map(self.read2)

        read1_positions = set(read1_map.keys())
        read2_positions = set(read2_map.keys())

        overlap_positions = read1_positions.intersection(read2_positions)

        sequencing_errors = list()
        for position in overlap_positions:
            if read1_map[position] != read2_map[position]:
                sequencing_errors.append(position)

        return sequencing_errors
