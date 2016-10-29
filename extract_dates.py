# coding=utf-8
import re
import datetime
import calendar
from dateutil import parser


VALID = [m for m in calendar.month_name]
SEPARATOR = '-'
DFLT_DATE = datetime.datetime(9999, 01, 01)


def extract_parens(text):
    #  Stackoverflow: re.findall('\(.*?\)',s)
    #  parens = re.findall(r'\(.*?\)+', text)    # This keeps the outer parens

    # Note: Regex doesn't like newlines, text should be cleaned of them before this.
    parens = re.findall(r'\((.*?)\)+', text)  # Discard the parentheses
    return parens


def is_integer(num):
    """
    Returns True if the num argument is an integer, and False if it is not.
    """
    try:
        num = float(num)
    except:
        return False

    return num.is_integer()


def date_component(text):
    if is_integer(text):
        return True
    elif text in VALID:
        return True
    elif text in ['–', '-']:  # Separators
        return True
    else:
        return False


def clean_string(text):
    NOISE = ['.', ',', ';', '?', '\xc2\xa0']
    for n in NOISE:
        text = text.replace(n, ' ')

    # Non-breaking hyphen, figure dash, en dash, em dash
    DASHES = ['--', '-', '\xe2\x80\x91', '\xe2\x80\x92', '\xe2\x80\x93', '\xe2\x80\x94']
    for d in DASHES:
        text = text.replace(d, ' - ')  # Normalize all the different dashes

    # Remove any parentheses(with content)
    #  text = re.sub(r'\(.*?\)', '', text)

    # Remove any footnotes(with anything inside)
    text = re.sub(r'\[.*?\]', '', text)

    # Remove any non-date text (keep only months, integers, and dash separators
    parts = text.split()
    stripped = [p.strip() for p in parts if date_component(p)]
    return ' '.join(stripped)


def parse_dates(text):
    # The default date fields - year is rediculous(9999) so it stands out.
    # Otherwise we use the first month and day as defaults. (Since we don't have requirements)

    dates = text.split(SEPARATOR)

    # Try to parse out the dates
    parsed_dates = []
    for d in dates:
        components = d.split()

        # Check for strange combos of years/
        if len(components) == 0:
            # Nothing to parse, and we don't want to add a placeholder
            continue
        if len(components) == 1:
            # We only have the year - is it a complete year? (4 digits?)
            year = components[0].strip()
            if len(year) != 4:
                # We'll ignore it since it's probably unreliable
                parsed_dates.append(None)
                continue

        parsed_dates.append(safe_parse(d))

    return parsed_dates


def safe_parse(d):
    try:
        date = parser.parse(d, default=DFLT_DATE)
        date = str(date.date())
        return date
    except ValueError as e:
        print('{} could not be parsed: {}'.format(d, e))
        # If we have stuff separated by long dashes, we'll assume it's probably a date, but
        # we just can't figure out exactly what it is, so we'll add None as a placeholder.
        return None


def scan_infoboxes(soup):
    """
    Check if there is an infobox table,
    """
    bday, dday = None, None
    # Check for the infobox,
    infobox = soup.find('table', {'class': 'infobox'})

    if infobox:
        # Try looking for the span with 'bday' class first
        bday_span = infobox.find('span', {'class': 'bday'})
        if bday_span:
            bday = str(parser.parse(bday_span.text, default=DFLT_DATE).date())

        dday_span = infobox.find('span', {'class': 'dday'})
        if dday_span:
            #  dday = parse_dates(dday_span.text)
            dday = str(parser.parse(dday_span.text, default=DFLT_DATE).date())

        # Try regex
        if not bday:
            bday = find_box_text(infobox, r'Born')
        if not dday:
            dday = find_box_text(infobox, r'Died')

    return [bday, dday]


def find_box_text(infobox, text):
    # Try regex
    result = infobox.find(text=re.compile(text))
    try:
        parent = result.parent
        td = parent.find_next()
        text = td.text.encode('utf-8')

        # Clean out parentheses(in infoboxes they usually hold the age, which we don't want)
        text = re.sub(r'\((.*?)\)', '', text)
        text = clean_string(text)
        text = [p for p in parse_dates(text) if p].pop()

    except:
        text = None

    return text


def parse_parentheses(text):
    parens = extract_parens(text)
    dates = []

    for p in parens:
        cleaned = clean_string(p)
        #  parsed = [p for p in parse_dates(cleaned) if p]
        parsed = [p for p in parse_dates(cleaned)]
        dates.extend(parsed)

    if len(dates) == 1:
        # Did we get the birth or death date??
        if text.find('died') >= 0:
            # Appears that they only have the date of death.
            return None, dates[0]
        else:
            # If it doesn't explicitly say "died" or maybe "passed away", we'll assume birth.
            return dates[0], None
    elif len(dates) == 2:
        # We got the birthdate and deathdate
        return dates[0], dates[1]

    elif len(dates) > 2:
        # We got more dates than we expected...
        # By default we'll use the first 2
        return dates[0], dates[1]
        #  return '???', '???'
    else:
        return None, None


def parse_text(text):
    # Try to parse the test for 'born' and 'died'
    born_i = text.find('born')
    died_i = text.find('died')

    # This section operates largely on the assumption that a birth date will follow the word "born YMD", and
    # that "died YMD" will follow after the born date in a block of text.
    try:
        if died_i >= 0:
            # Don't want conflict with death date.
            born_text = text[born_i:died_i]
        else:
            born_text = text[born_i:]
        bday = parse_dates(clean_string(born_text)).pop()
    except:
        bday = None

    try:
        died_text = text[died_i:]
        dday = parse_dates(clean_string(died_text)).pop()
    except:
        dday = None

    return [bday, dday]


def clean_initials(text):
    # Fix initials with period - wipe out the period
    #  initials = re.findall(r'\b([A-Z][.])+', text)
    initials = re.findall(r'\b([A-Z][.])', text)

    for i in initials:
        nodot = i.replace('.', '')
        text = re.sub(i, nodot, text)

    return text


def get_first_sentence(text):
    # Expand b. -> born
    text = text.replace('b.', 'born')

    # Expand d. -> '-' or separator character, this should help parse the dates.
    text = text.replace('d.', SEPARATOR)

    # Clean out initials
    text = clean_initials(text)

    # Clean out any terms that might disrupt getting the first sentence(any periods)
    NOISE = ['fl.', 'c.', 'tr.', '( listen)', '\n', '\r']
    for n in NOISE:
        text = text.replace(n, ' ')  # Space out dashs
    end = text.find('.')

    if end < 0:
        # There might not be a period...
        return text
    else:
        return text[:end]


def extract(text):
    """
    Extracts the dates from a block of text.
    """
    # Try to see if there are parentheses in the first sentence first.
    # If there is a parentheses with a date/year in it after the first sentence, it is MUCH LESS
    # likely to be a birth or death date.
    sentence1 = get_first_sentence(text)
    dates = parse_parentheses(sentence1)

    if any(dates):
        # Check for weird years
        if any('9999' in d for d in dates if d):
            pass  # We should try searching outside the parentheses
        else:
            return dates

    # Try searching the whole text
    return parse_text(text)
