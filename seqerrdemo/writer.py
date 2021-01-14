class SequencingErrorWriter(object):
    """
    A SequencingErrorWriter is an object that writes observations of
    sequencing errors to an output source.
    """
    def __init__(self, output):
        """
        Create a SequencingErrorWriter.
        :param output: the output sink to write to
        :raises ValueError: if output is not writable
        """
        if not output.writable():
            raise ValueError("output must be writable")

        self._output = output
        self._line_style = "{}\t{}\n"

    def write(self, query_name, positions):
        """
        Write an oberved set of sequencing errors.
        :param query_name: the query name of the read pair
        :param positions: the positions of the sequencing errors
        """
        positions = ",".join([str(i) for i in positions])
        line = self._line_style.format(query_name, positions)
        self._output.write(line)
