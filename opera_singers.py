#!/usr/bin/env python
# coding=utf-8
import extract_dates
import re
import scrapekit
from collections import namedtuple
Singer = namedtuple('Singer', ['firstname', 'lastname', 'voicetype', 'birthdate', 'deathdate', 'url'])

"""
These category pages list names that link to the full pages.
Data needs to be extracted and listed in an XML file as follows:

    First Name | Last Name | Voice Type | Birth Date | Date of Death
    - Dates format: YYYY-MM-DD
    - The voice type is derived from the category.
    - Getting a (200px * 200px minimum) portrait for each that can be imported properly,
      let us know and we'll discuss a different price.
"""

# Each opera singer link has:
#   a title="Opera Single Name", within an <a> tag
#   Lies within a <ul> in a <li>
# We could take a few approaches:
#   1 - Get all <a> tags and filter them by title
#   2 - Get all <li> and filter by <a> tags


ROOT = 'https://en.wikipedia.org'
URLS = [
    'https://en.wikipedia.org/wiki/Category:Operatic_basses',
    'https://en.wikipedia.org/wiki/Category:Operatic_bass-baritones',
    'https://en.wikipedia.org/wiki/Category:Operatic_baritones',
    'https://en.wikipedia.org/wiki/Category:Operatic_tenors',
    'https://en.wikipedia.org/wiki/Category:Operatic_countertenors',
    'https://en.wikipedia.org/wiki/Category:Castrati',
    'https://en.wikipedia.org/wiki/Category:Operatic_contraltos',
    'https://en.wikipedia.org/wiki/Category:Operatic_mezzo-sopranos',
    'https://en.wikipedia.org/wiki/Category:Operatic_sopranos',
]

# Note: https://en.wikipedia.org/wiki/Alexandrov_Ensemble_soloists
# This URL is not a particular singer, but a collection of people who performed with him.


def get_subcategories(soup):
    # Extra: Finds the sub-category links, not required, but maybe for the future
    subs = soup.find(id='mw-subcategories')
    links = subs.findAll('a')
    return links


def get_links1(soup):
    # Scrape the links from a category page
    # Find all the links under the "Pages in category: xxx", then filter by 'title' class.
    pagesection = soup.find(id='mw-pages')
    a_links = pagesection.findAll('a')

    a_links = [l['href'] for l in a_links if l.attrs.get('title', None)]
    return [ROOT + l for l in a_links if ':' not in l]


def get_links2(soup):
    # Scrape the links from a category page
    # Find all the list items, then filter out the ones that have an <a> child.
    pagesection = soup.find(id='mw-pages')
    listitems = pagesection.findAll('li')
    a_links = []
    for li in listitems:
        atag = li.find('a')
        if atag:
            a_links.append(ROOT + atag['href'])
    return a_links


def get_links3(soup):
    # Find the "Pages in category: xxx", section
    pagesection = soup.find(id='mw-pages')

    # Then go through all the group sections,
    groups = pagesection.findAll('div', {'class': 'mw-category-group'})

    links = []
    for g in groups:
        # We only want groups listed alphabetically (ex: 'A', 'B', etc)
        header = g.h3.text
        if header.isalpha() and header.isupper():

            links.extend(g.findAll('a'))

    # then filter by 'title' class.
    links = [l['href'] for l in links if l.attrs.get('title', None)]

    # Prepend the ROOT URL before returningthe list.
    return [ROOT + l for l in links if ':' not in l]


def get_page_counts(url):
    # Finds how many pages should be on the current page and returns it as an int.
    soup = scrapekit.handle_url(url)
    pages_span = soup.find(id='mw-pages')
    regex = r'The following [0-9]* pages are in this category, out of [0-9]* total.'
    nav_str = pages_span.find(text=re.compile(regex))

    #  results = re.search(r'[0-9]*', str(nav_str))
    results = re.findall(r'\d+', str(nav_str))
    assert len(results) == 2  # We should only have 2 integers from this.
    return int(results[0]), int(results[1])  # currentpage, total


def category_links(url):
    links = []
    while True:
        print('Scraping url: {}'.format(url))
        soup = scrapekit.handle_url(url)
        links.extend(get_links3(soup))

        nexturl = scrapekit.more_pages(soup, '(next page)')
        print('nexturl: {}'.format(nexturl))

        if nexturl:
            url = ROOT + nexturl
        else:
            break

    return links


def parse_voicetype(url):
    # Parse the voice type text from the url
    cutoff = url.find(':', 6) + 1  # Ignore first ':'
    return url[cutoff:].replace('_', ' ')


def parse_name(url):
    name = url.split('/')[-1]  # The singer name is last part of the url

    # Watch out for parentheses, (bass), (broadcaster), etc don't count. Should be removed.
    name = re.sub(r'\(.*?\)', '', name)

    # Split by underscore(url separator), make sure None doesn't get included!
    parts = [p for p in name.split('_') if p]

    # 'Alexandrov Ensemble soloists' doesn't count as as singer.
    if parts[-1] == 'soloists':
        return []
    else:
        return parts


def build_db(category_urls):
    singers = []

    for u in category_urls:
        vt = parse_voicetype(u)

        singer_links = category_links(u)
        print('Found {} singer links to parse through!'.format(len(singer_links)))

        for s in singer_links:
            print('Getting info for: {}'.format(s))
            soup = scrapekit.handle_url(s)
            name = parse_name(s)

            if name is None or len(name) == 0:
                print('Skipping, name not valid.')
                continue

            # Check infoboxes first
            dates = extract_dates.scan_infoboxes(soup)

            if not any(dates):
                # Check first paragraph
                p = soup.find(id='mw-content-text').p
                p_text = p.text.encode('utf-8')
                dates = extract_dates.extract(p_text)

            singer_nt = Singer(
                firstname=name[0],
                lastname=name[-1],
                voicetype=vt,
                birthdate=dates[0],
                deathdate=dates[-1],
                url=s,
            )
            print(singer_nt)
            singers.append(singer_nt)
    return singers


def link_counts(urls):
    singers = {}  # voicetype: listoflinks, total count(what wikipedia is saying..)

    for u in urls:
        # Get counts for verification
        count, total = get_page_counts(u)
        voicetype = parse_voicetype(u)
        singers[voicetype] = category_links(u), total

    return singers


def category_counts_and_summary():
    links = link_counts(URLS)

    print('{:25}{:>10}{:>10}'.format('Voice type:', 'Count:', 'Expected'))
    total_count = 0
    for k, v in links.items():
        print('-'*80)
        singers, total = v
        print('{:25}{:>10}{:>10}'.format(k, len(singers), total))

        if total != len(singers):
            print('\tCounts do not match!')

        #  for i in singers:
            #  print(i)

        print('')
        total_count += total

    print('{} singer links found in all category pages.'.format(total_count))


if __name__ == "__main__":
    #  category_counts_and_summary()
    test_urls = URLS
    print(test_urls)

    singer_nts = build_db(test_urls)

    print('')
    print('Found these:')
    for s in singer_nts:
        print(s)

    FILENAME = 'data/singers_all.xml'
    import format_singers
    format_singers.make_xml(FILENAME, singer_nts)
