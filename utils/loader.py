import os, os.path
import models.forms as forms

def get_dirs(path):
    result = []
    for f in os.listdir(path):
        p = os.path.join(path, f)
        if os.path.isdir(p):
            result.append(p)

    return result

def get_forms():
    return forms.models

def load_corpus(path):
    result = []
    for f in os.listdir(path):
        if f.endswith(".txt"):
            with open(os.path.join(path, f), 'r') as fh:
                result.append(fh.read())
    return result

