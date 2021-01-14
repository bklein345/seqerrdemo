import sys
from argparse import ArgumentParser

from pysam.libcalignmentfile import AlignmentFile

from seqerrdemo.iterator import PredicatedReadIterator, PairedReadIterator
from seqerrdemo.predicate import MappingQualityPredicate, UnionPredicate, OverlappingReadPairPredicate
from seqerrdemo.read_pair import ReadPair
from seqerrdemo.writer import SequencingErrorWriter


class SequencingErrorController(object):
    """
    A SequencingErrorController represents a controller for the
    collection of sequencing error observations from an alignment file.
    """

    def __init__(self, af, predicate, output):
        """
        Create a SequencingErrorController.
        :param af: the AlignmentFile to gather sequencing errors from
        :param predicate: the predicate to apply to reads to determine
        if they are evaluated.
        :param output: the output to write observations to
        """
        self._iterator = PairedReadIterator(PredicatedReadIterator(af, predicate))
        self._writer = SequencingErrorWriter(output)

    def go(self):
        """
        Gather sequencing errors and write them to output.
        """
        for read1, read2 in self._iterator:
            read_pair = ReadPair(read1, read2)
            query_name = read_pair.query_name
            sequencing_error_positions = read_pair.get_sequencing_errors()

            if len(sequencing_error_positions) > 0:
                self._writer.write(query_name, sequencing_error_positions)


# Types to use for parsing
def _readable_bam_file(arg):
    # Note that an argument of '-' is interpreted as sys.stdin by pysam
    return AlignmentFile(arg, 'r')


def _output_file_or_stdout(arg):
    if arg == '-':
        return sys.stdout
    return open(arg, 'w')


def main(args_list=None):
    if args_list is None:
        args_list = sys.argv[1:]

    parser = ArgumentParser("Gather and report observations of sequencing errors.")

    parser.add_argument("--input", type=_readable_bam_file,
                        help="Input Alignment File. (- for stdin)",
                        required=True)
    parser.add_argument("--output", type=_output_file_or_stdout,
                        help="Output File. (- for stdout)",
                        required=True)
    parser.add_argument("--min_mapping_quality", type=int,
                        help="Minimum mapping quality for a read to be considered.",
                        required=False, default=20)

    args = parser.parse_args(args_list)

    predicate = UnionPredicate()
    predicate.add(MappingQualityPredicate(args.min_mapping_quality))
    predicate.add(OverlappingReadPairPredicate())

    controller = SequencingErrorController(args.input, predicate, args.output)
    controller.go()


if __name__ == "__main__":
    main()
