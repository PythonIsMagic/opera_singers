# coding=utf-8
from bs4 import BeautifulSoup
import os
import re
import requests
import urlparse
import time

DELAY = 1  # Seconds
DATADIR = "data/"
PAGEDIR = "./pages/"

HEADER_MOZ1 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5)'}
HEADER_MOZ2 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) \
               AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
               "Accept": "text/html,application/xhtml+xml,application/xml;\
               q=0.9,image/webp,*/*;q=0.8"}


def saved_html_name(url):
    parsed = urlparse.urlparse(url)
    filename = parsed.netloc + parsed.path + parsed.query
    if not filename.endswith('.html'):
        filename += '.html'

    # We cannot use '/' in our names - conflicts with Linux. Use '__' instead.
    filename = filename.replace('/', '__')
    return PAGEDIR + filename


def save_html(url):
    # We will save the file as the url if possible.
    req = requests.get(url, headers=HEADER_MOZ1)

    if req.ok:
        time.sleep(DELAY)  # Be polite! ;)
        html = req.text
    else:
        print('Request unsuccessful with code: {}'.format(req.status_code))
        return None

    if html:
        ensure_dir(PAGEDIR)
        filename = saved_html_name(url)

        with open(filename, 'w') as f:
            f.write(html.encode('utf-8'))
        return html
    else:
        print('Not able to retrieve and save html!')
        return None


def load_html(url):
    filename = saved_html_name(url)

    # If file is empty, just delete it
    if os.path.exists(filename) and os.path.getsize(filename) == 0:
        os.remove(filename)

    # Check if file exists and return the html
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read()
    else:
        return None


def handle_url(url):
    # Checks if the URL exists as a saved html file, and returns it's soup.
    # If we don't have it, we download it and save it. And return it's soup.

    # dir is a subdir of PAGEDIR.
    # timestamp - useful if we want to keep checking updated versions.
    # overwrite - if we always want the newest ver.
    html = load_html(url)

    if not html:
        print('Downloading {}.'.format(url))
        html = save_html(url)
    else:
        print('HTML on file.')

    if html:
        return BeautifulSoup(html, "html.parser")
    else:
        print('Problem generating soup!')
        return None


def ensure_dir(_dir):
    if not os.path.exists(_dir):
        os.makedirs(_dir)


def more_pages(soup, text):
    # Return True if there is a link with the text in it (usually something like "more" or
    # "next page")
    # Return the link, or None

    results = soup.findAll(text=re.compile(r'{}'.format(text)))

    for r in results:
        parent = r.parent

        if parent and parent.name == 'a':
            return parent['href']
    return None
