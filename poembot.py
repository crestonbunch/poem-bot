import configparser
import random
from models.styles import *
from models.forms import *
from utils import loader
from utils.trainer import Trainer
from utils.pipeline import Pipeline

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PoemBot:

    def __init__(self, config, builder):
        self.config_path = config
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.builder = builder
        self.forms = loader.get_forms()
        self.forms_store = builder.get_object('forms_list_store')
        self.styles = loader.get_dirs('data')
        self.styles_store = self.builder.get_object('styles_list_store')
        self.config_store = builder.get_object('config_tree_store')
        self.poem_view = builder.get_object('poem_view')
        self.window = self.builder.get_object('main_window')
        self.window.connect('delete-event', Gtk.main_quit)

        self.handlers = {
            'select_style': self.select_style,
            'select_form': self.select_form,
            'edit_config': self.edit_config,
            'train_models': self.train_models,
            'build_poem': self.build_poem
        }

    def select_style(self, widget, path):
        self.styles_store[path][1] = not self.styles_store[path][1]

    def select_form(self, widget, path):
        self.forms_store[path][2] = not self.forms_store[path][2]

    def edit_config(self, widget, path, text):
        row = self.config_store[path]
        if row.parent is not None: # can't edit top-level rows
            row[1] = text
            # save new config file
            self.config[row.parent[0]][row[0]] = text
            with open(self.config_path, 'w') as fh:
                self.config.write(fh)

    def train_models(self, *args):
        # initialize models
        p_len = self.config['VocabularyModel'].getint('PrefixSize')
        s_len = self.config['VocabularyModel'].getint('SuffixSize')
        regex = self.config['Tokenizer'].get('Regex')
        self.vocab_model = VocabularyModel(p_len, s_len, regex)

        # load corpus
        style_corpus = []
        for path in self._get_styles():
            style_corpus += loader.load_corpus(path)

        # train style models
        self.trainer = Trainer(style_corpus, self.vocab_model)
        self.trainer.on_update(self._update_progress)
        self.trainer.train_all()

    def build_poem(self, *args):
        self.form_model = self._pick_form()()

        self.pipeline = Pipeline(
            self.vocab_model.weight,
            self.form_model.weight
        )

        # start the state as the empty string
        state = ['']
        # start with no known transitions
        transitions = []

        for i in range(50):
            state += self._pick(self.pipeline.pipe(state, transitions))

        self.poem_view.get_buffer().set_text(' '.join(state))

    def start(self):
        self._load_styles()
        self._load_forms()
        self._load_config()
        self.builder.connect_signals(self.handlers)
        self.window.show_all()
        Gtk.main()

    def _update_progress(self):
        pass

    def _pick(self, options):
        """Pick a choice from a list of weighted options.

        Arguments:
            options: A list of (choice, probability) tuples. Where probability
                is within [0, 1] and the sum of all probabilities is [0, 1]
        """
        roll = random.random()

        result = None
        cumsum = 0
        while cumsum < roll and options:
            result = options.pop()
            cumsum += result[1]

        return result[0]

    def _get_styles(self):
        """Get the selected style paths."""
        paths = []
        for row in self.styles_store:
            if row[1]: paths.append(row[0])
        return paths

    def _get_forms(self):
        """Get the selected forms."""
        paths = []
        for row in self.forms_store:
            if row[2]: paths.append(globals()[row[1]])
        return paths

    def _load_styles(self):
        for s in self.styles:
            self.styles_store.append((s, False))

    def _load_forms(self):
        for f in self.forms:
            self.forms_store.append((f.name, f.__name__, False))

    def _load_config(self):
        for section in self.config.sections():
            piter = self.config_store.append(None, (section,''))
            for key in self.config[section]:
                val = self.config[section][key]
                self.config_store.append(piter, (key, val))

    def _pick_form(self):
        """Pick a random selected form."""
        return random.choice(self._get_forms())

    def _on_update(self):
        pass


if __name__ == '__main__':

    builder = Gtk.Builder()
    builder.add_from_file('res/main.glade')

    bot = PoemBot('config.ini', builder)
    bot.start()
