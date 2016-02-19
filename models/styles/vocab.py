import random
from nltk.tokenize import word_tokenize, RegexpTokenizer

class VocabularyModel:
    """A markov model that learns a poet's vocabulary."""

    def __init__(self, p_len, s_len, regex):
        """Initialize the vocabulary model. Begin with an empty transition
        matrix. The matrix is represented as a dictionary of dictionaries. This
        makes online learning much easier.

        Arguments:
            p_len: The length of the prefix size in the markov chain.
            s_len: The length of the suffix size in the markov chain.
            regex: The token regex to use for our tokenizer.
        """
        self.transitions = {'':{}}
        self.tokenizer = RegexpTokenizer(regex)
        self.p_len = p_len
        self.s_len = s_len

    def train(self, text):
        """Build a markov model from the given text. Supports online learning,
        so it will improve an existing model rather than delete it."""
        tokens = self._tokenize(text)

        for p, s in self._find_states(tokens, self.p_len, self.s_len):
            self._add_sample(p, s)

    def predict(self, state):
        """Predict the next state given the current state."""
        options = list(self.transitions[state].keys())
        total = sum(list(self.transitions[state].values()))
        roll = random.randint(0, total)

        result = None
        cumsum = 0
        while cumsum < roll:
            result = options.pop()
            cumsum += self.transitions[state][result]

        return result

    def weight(self, state, transitions):
        """Return a list of transition probabilities given the current state.
        This is normally the first step in a pipeline, and so the transitions
        are initially empty and ignored by this model.

        Arguments:
            state: The list of tokens in the current state.
            transitions: This argument is ignored, and a new list of transitions
                is returned by the vocab model.

        Returns:
            A list of tuples, where the first element is the next state and the
            second element is the probability of reaching that state.
        """
        # take only the last part of the state that is our prefix length, and
        # cast it to a tuple so it is hashable for our dictionary
        state = tuple(state[-self.p_len:])
        try:
            options = list(self.transitions[state].keys())
            total = sum(list(self.transitions[state].values()))
            result = []
            for o in options:
                p = self.transitions[state][o] / total
                result.append((o, p))
            return result
        except KeyError as e:
            print(e)
            return [('', 1.0)]

    def _tokenize(self, s):
        return self.tokenizer.tokenize(s)

    def _add_sample(self, p, n):
        if p not in self.transitions:
            self.transitions[p] = {}

        if n not in self.transitions[p]:
            self.transitions[p][n] = 0

        self.transitions[p][n] += 1


    def _find_states(self, seq, p_len, s_len):
        """Build a list of prefix states and suffix states from the given
        sequence of tokens.

        Arguments:
            seq: A sequence of tokens to build states out of.
            p_len: The length of the prefixes
            s_len: The length of the suffixes

        Returns:
            A list of tuples, where the first item in each tuple is the prefix
            and the second item is the suffix.
        """
        result = []

        # start with a prefix buffer of the empty string
        p_buffer = ['']
        # start with a suffix buffer of the first few tokens
        s_buffer = seq[:s_len]

        # copy the buffers to the result
        result.append((tuple(p_buffer), tuple(s_buffer)))

        # go through each token, update the buffers, and add them to the result
        for n in seq[s_len:]:
            # move the p_buffer
            if len(p_buffer) >= p_len:
                p_buffer.pop(0)
            # move the s_buffer
            p_buffer.append(s_buffer.pop(0))
            s_buffer.append(n)
            # copy the buffers to the result
            result.append((tuple(p_buffer), tuple(s_buffer)))

        return result
