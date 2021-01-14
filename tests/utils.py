from collections import OrderedDict

from pysam.libcalignedsegment import AlignedSegment
from pysam.libcalignmentfile import AlignmentHeader


def _make_test_read(query_name="query", mapping_quality=20, template_length=10,
                    query_length=5, is_proper_pair=True, is_read1=True):
    flag = 1
    if is_proper_pair:
        flag += 2
    if is_read1:
        flag += 64

    read = {
        'name': query_name,
        'flag': str(flag),
        'ref_name': '1',
        'ref_pos': '10',
        'map_quality': str(mapping_quality),
        'cigar': str(query_length) + 'M',
        'next_ref_name': '=',
        'next_ref_pos': '1',
        'length': str(template_length),
        'seq': 'A'*query_length,
        'qual': 'I'*query_length,
        'tags': ['MD:Z:1']
    }
    header = AlignmentHeader.from_dict(OrderedDict([
        ('HD', {'VN': '1.6', 'GO': 'none', 'SO': 'coordinate'}),
        ('SQ', [{'SN': '1', 'LN': 249250621}])
    ]))

    return AlignedSegment.from_dict(read, header)


class _FakeAlignmentFile(object):
    def __init__(self):
        self.reads = list()

    def add_read(self, read):
        self.reads.append(read)

    def fetch(self):
        for read in self.reads:
            yield read


class _MockOutput(object):
    def __init__(self, writable=True):
        self.output = ""
        self.is_writable = writable

    def writable(self):
        return self.is_writable

    def write(self, towrite):
        self.output += towrite
