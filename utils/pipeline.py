class Pipeline:
    """This class represents a pipeline for the poem bot. By giving it a series
    of connected models, it provides an interface to build a poem."""

    def __init__(self, *args):
        """Initialize the pipeline with a list of functions to execute.

        Arguments:
            Each argument is a function that takes in a current state, and a
            list of transition tuples (next state, probability) and outputs
            a modified list of transition tuples.
        """
        self.pipeline = args

    def pipe(self, state, transitions):
        """Pipe a state and transition vector through the pipeline, and return
        the output.

        Arguments:
            state: The current state of the model, usually a list of strings.
            transitions: A list of tuples where the first element of a tuple is
                the next state, and the second element is the probability of
                reaching that state.

        Returns:
            A new list of transitions after running the list through each
            function in the pipeline sequentially.
        """

        for f in self.pipeline:
            transitions = f(state, transitions)

        return transitions
