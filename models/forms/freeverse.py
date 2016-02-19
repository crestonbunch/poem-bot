
class FreeVerseModel:
    """This class describes a free verse poetry form in a way that it
    can weight next states given a state, where the next state is a
    word and the previous state is all the previous words in a poem."""

    name = "Free Verse"

    def __init__(self):
        pass

    def weight(self, current_state, transitions):
        """Anything goes in a free verse poem."""

        return transitions
