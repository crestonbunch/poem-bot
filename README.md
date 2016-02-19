Poem Bot
========

Installation
------------

This program is written in Python 3 with the following packages:

    PyGI
    NLTK
    requests
    PRAW (optional, used for Reddit scraper)
    ProgressBar (optional, used for Reddit scraper)

Quickstart
----------

1. From the terminal ```cd``` to the poem-bot directory.
2. ```mkdir data```
3. Fill the data directory with more directories. For example: create separate
   directories for individual poets, or for styles of poetry.
4. Fill these directories with poems in text files that have the
   ```.txt``` extension.
5. From the command line you can use ```python poembot.py``` to start the GUI.
6. On the left select 1 or more training sets and 1 or more poetic forms.
7. Hit the "Train" and wait for it to finish training.
8. Hit the "Generate" button to generate a poem.

What works
----------

A basic markov model for training and generating poems from input. Some GUI
elements for configuring the bot.

What is in progress
-------------------

* More models to incorporate into the pipeline such as part-of-speech tagging,
  poetic forms to enforce meter and rhyme, etc.
* Integration with the Datamuse API for rhymes and synonyms and other
  enhancements it can provide.
* Integration with the Wordnik API for information on word syllables and
  stresses for tracking meter and syllable counts.
* GUI features for examining a poem and looking at why the bot chose each
  word and third-party API outputs for each word.

Want to help?
-------------

Just fork and submit a pull request. I'll review it and if it looks good, then
merge it in.

License
-------

MIT
