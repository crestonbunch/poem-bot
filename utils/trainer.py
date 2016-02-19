from multiprocessing import Process

class Trainer:
    """This class helps train models, spawing multiple processes to do it
    faster."""

    def __init__(self, data, *args):
        """Initialize a trainer with training data and models to train."""
        self.data = data
        self.models = args
        self.callback = lambda x: x

    def on_update(self, callback):
        """Bind a callback to run whenever the trainer status updates. Passes
        the percent [0, 1] to the callback function."""
        self.callback = callback

    def train_all(self):
        """Start training each model in a different process."""

        for model in self.models:
            f = lambda: self.train_one(model)
            f()
            #Process(target=f).start()
            print("Trained 1")

    def train_one(self, model):
        for sample in self.data:
            model.train(sample)
