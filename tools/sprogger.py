"""
This script uses PRAW to scrape all comments from /u/Poem_for_your_sprog off of
reddit.
"""

import praw
import argparse
import os.path
import webbrowser
import random
import hashlib
from progressbar import ProgressBar, Counter, Bar, Percentage

def save(text, location):
    with open(location, 'w') as fh:
        fh.write(text)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Scrape a famous reddit poet.")
    parser.add_argument('path',help='Directory to dump poems to.')
    parser.add_argument('app_id',help='Reddit app id')
    parser.add_argument('app_secret',help='Reddit app secret')

    args = parser.parse_args()

    r = praw.Reddit(user_agent="Sprogger 1.0")

    r.set_oauth_app_info(
        client_id=args.app_id,
        client_secret=args.app_secret,
        redirect_uri='http://127.0.0.1:65010/authorize_callback'
    )

    uniq = hashlib.sha256(str(random.random()).encode('utf-8')).hexdigest()
    url = r.get_authorize_url(uniq, 'identity read history', True)
    webbrowser.open(url)

    token = input("Enter token here: ")

    access_information = r.get_access_information(token)
    r.set_access_credentials(**access_information)

    user = r.get_redditor("Poem_for_your_sprog")

    print("Downloading...")
    comments = list(user.get_comments(sort='top', time='all', limit=1000))

    widgets = [Counter(), '/', str(len(comments)), ' ',
               Percentage(), ' ', Bar()]
    bar = ProgressBar(max_value=len(comments), widgets=widgets).start()

    for i,c in enumerate(comments):
        save(c.body, os.path.join(args.path, str(i+1) + ".txt"))
        bar.update(i + 1)

    bar.finish()
