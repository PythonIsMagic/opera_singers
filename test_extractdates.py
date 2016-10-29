# coding=utf-8
import extract_dates as ed
import pytest
import scrapekit

"""
Tests for extract(text)
"""


def test_extract_DMY_longdash():
    d = ed.extract('Ellen Gulbranson (4 March 1863 – 2 January 1947)')
    assert d[0] == '1863-03-04'
    assert d[1] == '1947-01-02'


def test_extract_DMY_shortdash():
    d = ed.extract('Name (20 December 1928 - 8 April 1996)')
    assert d[0] == '1928-12-20'
    assert d[1] == '1996-04-08'


def test_extract_DMY_footnote():
    d = ed.extract('(22 February 1910, Whitstable - 12 January 1982, Croydon[1])')
    assert d[0] == '1910-02-22'
    assert d[1] == '1982-01-12'


def test_extract_DMY_footnotes():
    d = ed.extract('(10 October 1894[1][2] – 29 January 1972)')
    assert d[0] == '1894-10-10'
    assert d[1] == '1972-01-29'


def test_extract_DMY_locations():
    d = ed.extract('(27 January 1908, Stuttgart – 18 October 1997, Stuttgart)')
    assert d[0] == '1908-01-27'
    assert d[1] == '1997-10-18'


def test_extract_DMY_Y():
    d = ed.extract('(17 October 1778 – after 1828 )')
    assert d[0] == '1778-10-17'
    assert d[1] == '1828-01-01'


def test_extract_MDY_dash():
    d = ed.extract('Name (June 13, 1838 - August 11, 1914)')
    assert d[0] == '1838-06-13'
    assert d[1] == '1914-08-11'


def test_extract_MDY_longdash():
    d = ed.extract('(May 8, 1863 in Turin – May 4, 1943 in Pollone)')
    assert d[0] == '1863-05-08'
    assert d[1] == '1943-05-04'


def test_extract_Y_MY():
    d = ed.extract("(also Andrien, or Adrien l'Ainé; 1766-November 1823)")
    assert d[0] == '1766-01-01'
    assert d[1] == '1823-11-01'


def test_extract_Y_Y_longdash():
    d = ed.extract('(1754–1829)')
    assert d[0] == '1754-01-01'
    assert d[1] == '1829-01-01'


def test_extract_Y_Y_dash():
    d = ed.extract('(1889-1932)')
    assert d[0] == '1889-01-01'
    assert d[1] == '1932-01-01'


def test_extract_borndate_MDY():
    d = ed.extract('(born February 25, 1981)')
    assert d[0] == '1981-02-25'
    assert d[1] == None


def test_extract_borndate_DMY():
    d = ed.extract('(born 15 March 1954)')
    assert d[0] == '1954-03-15'
    assert d[1] == None


def test_extract_borndate_DMY_loc():
    d = ed.extract('(born 25 July 1946, Bratislava)')
    assert d[0] == '1946-07-25'
    assert d[1] == None


def test_extract_borndate_MDY_loc():
    d = ed.extract('Lawrence Zazzo (born December 15, 1970 in Philadelphia) is an American countertenor.')
    assert d[0] == '1970-12-15'
    assert d[1] == None


def test_extract_bornyear():
    d = ed.extract('(born 1971)')
    assert d[0] == '1971-01-01'
    assert d[1] == None


def test_extract_bornyear_loc():
    d = ed.extract('Matthew White (born 1973 in Ottawa, Ontario) is a Canadian countertenor.')
    assert d[0] == '1973-01-01'
    assert d[1] == None


def test_extract_years_with_locs():
    d = ed.extract('Henri Ledroit (Villacourt, 1946 - Nancy, France, 1988) was a French counter-tenor.')
    assert d[0] == '1946-01-01'
    assert d[1] == '1988-01-01'


def test_extract_borndate_junkparens():
    d = ed.extract('Yoshikazu Mera (米良 美一 Mera Yoshikazu?), born May 21, 1971, in Miyazaki, Japan, is a Japanese countertenora')
    assert d[0] == '1971-05-21'
    assert d[1] == None


def test_extract_2parens_dates():
    d = ed.extract('(or Nikolai Gjaurov, Nikolay Gyaurov, Bulgarian: Николай Гяуров) (September 13, 1929 – June 2, 2004)')
    assert d[0] == '1929-09-13'
    assert d[1] == '2004-06-02'


def test_extract_bothdates_semicolon():
    # https://en.wikipedia.org/wiki/Jules_Bastin
    d = ed.extract('Jules Bastin (18 August 1933 – 2 December 1996; Waterloo) was a Belgian operatic bass.')
    assert d[0] == '1933-08-18'
    assert d[1] == '1996-12-02'


def test_extract_bornyear_incomplete():
    # https://en.wikipedia.org/wiki/Marco_Arati
    #  import pdb; pdb.set_trace()
    d = ed.extract('Marco Arati (181? - 1899) was an Italian operatic bass active during the 1840s through the 1880s.')
    assert d[0] == None
    assert d[1] == '1899-01-01'


def test_extract_bornyear_noparens_stillalive():
    d = ed.extract('Anja Kampe is a German-Italian operatic soprano, born 1968 in the GDR.')
    assert d[0] == '1968-01-01'
    assert d[1] == None


def test_extract_dates_not_in_parens():
    d = ed.extract('Jeanne Anaïs Castellan (real name Jeanne Anaïs Castel or Chastel), born in Beaujeu, Rhône on 26 October 1819, died in Paris 1861,')
    assert d[0] == '1819-10-26'
    assert d[1] == '1861-01-01'


def test_extract_nodates_stillalive():
    d = ed.extract("Vlada Borovko is a Russian operatic soprano.")
    assert d[0] == None
    assert d[1] == None


def test_extract_nodates_dead():
    d = ed.extract("Janice L Chapman AUA MOA was a distinguished Australian-born soprano")
    assert d[0] == None
    assert d[1] == None


def test_extract_nodates_withparens():
    # https://en.wikipedia.org/wiki/Thierry_Gr%C3%A9goire
    d = ed.extract('Thierry Grégoire (Charleville-Mézières) is a French countertenor.[1]')
    assert d[0] == None
    assert d[1] == None


def test_extract_dieddate():
    # https://en.wikipedia.org/wiki/Fran%C3%A7ois_Beaumavielle
    d = ed.extract('François Beaumavielle (died 1688, Paris) was a French operatic bass-baritone.')
    assert d[0] == None
    assert d[1] == '1688-01-01'


def test_extract_bornpre1900():
    # https://en.wikipedia.org/wiki/Norman_Allin
    #  import pdb; pdb.set_trace()
    d = ed.extract('Norman Allin (19 November 1884 – 27 October 1973) was a British bass singer of the early and mid twentieth century, and later a teacher of voice.')
    assert d[0] == '1884-11-19'
    assert d[1] == '1973-10-27'


def test_extract_problemtext():
    # https://en.wikipedia.org/wiki/Kim_Borg
    p = """Kim Borg (August 7, 1919 – April 28, 2000) was a Finnish bass, teacher and composer.
    He had a wide-ranging, resonant, warm voice.[1]
    """

    d = ed.extract(p)
    assert d[0] == '1919-08-07'
    assert d[1] == '2000-04-28'


def test_extract_problemparagraph():
    # https://en.wikipedia.org/wiki/Owen_Brannigan
    p = """Owen Brannigan OBE (10 March 1908 – 9 May 1973) was an English bass, known in opera for
    buffo roles and in concert for a wide range of solo parts in music ranging from Henry Purcell to
    Michael Tippett. He is best remembered for his roles in Mozart and Britten operas and for his
    recordings of roles in Britten, Offenbach and Gilbert and Sullivan operas, as well as recordings
    of English folk songs.
    """

    d = ed.extract(p)
    assert d[0] == '1908-03-10'
    assert d[1] == '1973-05-09'


def test_extract_problemparagraph2():
    # https://en.wikipedia.org/wiki/Adamo_Didur
    p = """Adam Didur or Adamo Didur[1] (24 December 1874 – 7 January 1946) was a famous Polish
    operatic bass singer.[2][3][4] He sang extensively in Europe and had a major career at New
    York's Metropolitan Opera from 1908 to 1932."""

    d = ed.extract(p)
    assert d[0] == '1874-12-24'
    assert d[1] == '1946-01-07'


def test_extract_problemparagraph3():
    # https://en.wikipedia.org/wiki/David_Franklin_(broadcaster)
    d = ed.extract('David Franklin (17 May 1908 – 22 October 1973) was a British opera singer and broadcaster.')
    assert d[0] == '1908-05-17'
    assert d[1] == '1973-10-22'


def test_extract_middle_initial_period():
    # https://en.wikipedia.org/wiki/Jerome_Hines

    p = """Jerome A. Hines (November 8, 1921 – February 4, 2003) was an American operatic bass
    who performed at the Metropolitan Opera from 1946-87. Standing 6'6", his stage presence and
    stentorian voice made him ideal for such roles as Sarastro in The Magic Flute,
    Mephistopheles in Faust, Ramfis in Aida, the Grand Inquisitor in Don Carlos, the title role
    of Boris Godunov and King Mark in Tristan und Isolde."""
    #  import pdb; pdb.set_trace()
    d = ed.extract(p)
    assert d[0] == '1921-11-08'
    assert d[1] == '2003-02-04'


def test_extract_abbreviatedyear():
    # https://en.wikipedia.org/wiki/Antonio_Francesco_Carli
    d = ed.extract('Antonio Francesco Carli (fl. 1706–23) was an Italian bass singer, primarily of operatic roles.')
    assert d[0] == '1706-01-01'
    assert d[1] == None


def test_extract_over3dates():
    # https://en.wikipedia.org/wiki/Kaspar_Bausewein
    p = """Kaspar Bausewein (15 November 1838, Aub – 18 November 1903, Munich) was a German
    operatic bass who was active at the Bavarian State Opera from 1858 through 1900. While
    there, he notably portrayed several characters in the world premieres of operas composed by
    Richard Wagner. He created Pogner in Die Meistersinger von Nürnberg (June 21, 1868), Fafner
    in Das Rheingold (September 22, 1869), Hunding in Die Walküre (June 26, 1870), and Harald in
    Die Feen (June 29, 1888).[1]"""

    d = ed.extract(p)
    assert d[0] == '1838-11-15'
    assert d[1] == '1903-11-18'


def test_extract_noiseinparens():
    # https://en.wikipedia.org/wiki/Armand_Castelmary
    p = """Armand Castelmary, real name Comte Armand de Castan, born Toulouse 16 August 1834,
    died New York City 10 February 1897, was a French operatic bass. He created roles in three
    major premieres at the Paris Opera – Don Diego in L'Africaine by Meyerbeer (1865), the Monk
    in Verdi's Don Carlos (1867), and Horatio in Ambroise Thomas's Hamlet (1868). Castelmary
    also appeared at opera houses in England and the United States, and died onstage at the
    Metropolitan Opera House, New York, during a performance of Martha by Friedrich von
    Flotow.[1]"""

    d = ed.extract(p)
    assert d[0] == '1834-08-16'
    assert d[1] == '1897-02-10'


def test_extract_multipledates():
    # https://en.wikipedia.org/wiki/Stefan_Dimitrov_(bass)

    p = """Stefan Dimitrov (22 November 1939 – 13 August 2004 ) was a basso opera singer. Born
    in the Black Sea town of Burgas, Bulgaria, he was of Greek origin. He won four international
    singing competitions at the very beginning of his career: those in Toulouse, the "Erkel" in
    Budapest, the "s’Hertogenbosch" in the Netherlands, and the "Young Opera Singers" in Sofia.
    In 1965 Stefan Dimitrov met the piano accompanist and répétiteur, Malina Dimitrova (19 June
    1945 - 24 April 2008), who graduated at this time and took her first steps in the opera
    accompanying field. They were later to be married. The couple had one son, Liuben, who
    graduated as solo pianist and later become part of the Genova & Dimitrov piano duo."""

    d = ed.extract(p)
    assert d[0] == '1939-11-22'
    assert d[1] == '2004-08-13'


def test_extract_dates_outside_parens():
    # https://en.wikipedia.org/wiki/Louis_Baron
    #  import pdb; pdb.set_trace()
    p = """Louis Baron, (real name Louis Bouchêne, or Bouchenez), stage name Baron, was a French
    actor and singer (bass), born in September 1838 at Alençon, died in 1920.[1]"""

    d = ed.extract(p)
    assert d[0] == '1838-09-01'
    assert d[1] == '1920-01-01'


def test_extract_OR_indicating_unknown():
    p = """Francesco Carattoli (1704 or 1705 – March 1772) was an Italian bass buffo, or singer of
    opera buffa."""

    d = ed.extract(p)
    assert d[0] == None
    assert d[1] == '1772-03-01'


def test_extract_brackets_in_parens():
    p = """Feodor Ivanovich Chaliapin (Russian: Фёдор Ива́нович Шаля́пин, tr. Fëdor Ivanovič
    Šalâpin; IPA: [ˈfʲɵdər ɪˈvanəvʲɪtɕ ʂɐˈlʲapʲɪn] ( listen); February 13 [O.S. February 1] 1873
    – April 12, 1938) was a Russian opera singer. Possessing a deep and expressive bass voice,
    he enjoyed an important international career at major opera houses and is often credited
    with establishing the tradition of naturalistic acting in his chosen art form.[1]"""
    #  import pdb; pdb.set_trace()
    d = ed.extract(p)
    assert d[0] == '1873-02-13'
    assert d[1] == '1938-04-12'


def test_extract_deported():
    # https://en.wikipedia.org/wiki/Hans_Erl
    # This one is a little exceptional, but the wiki page says he probably died the same year
    # he was deported.
    #  import pdb; pdb.set_trace()
    p = 'Hans Tobias Erl (Warsaw or Vienna 1882 — Deported to Auschwitz, 1942?) was a German operatic bass.[1]'

    d = ed.extract(p)
    assert d[0] == '1882-01-01'
    assert d[1] == '1942-01-01'


def test_extract_has_b_and_d_period():
    # https://en.wikipedia.org/wiki/Karl_Formes
    p = """Karl Johann Franz Formes (b. Mülheim am Rhein, 7 August 1815; d. San Francisco, 15
    December 1889), also called Charles John Formes, was a German bass opera and oratorio singer
    who had a long international career especially in Germany, London and New York.[1]"""

    d = ed.extract(p)
    assert d[0] == '1815-08-07'
    assert d[1] == '1889-12-15'


def test_extract_has_unbalanced_parens():
    # https://en.wikipedia.org/wiki/Mikhail_Sariotti
    p = """Mikhail Sariotti (Russian: Михаил Иванович (or Яковлевич)[1]) Сариотти; 1839 (or
    1830, or 1831),[2][3] near of Vyborg (near Saint Petersburg) - January 30 (February 11)
    1878, Saint Petersburg) was a famous Russian opera singer (bass-baritone) and music
    critic."""
    d = ed.extract(p)
    assert d[0] == None
    assert d[1] == None


def test_extract_has_unbalanced_parens2():
    # https://en.wikipedia.org/wiki/Fyodor_Stravinsky

    p = """Fyodor Ignatievich Stravinsky (Russian: Фёдор Игна́тиевич Страви́нский), 20 June [O.S.
    8 June] 1843, in Halavintsy, Minsk Governorate  – 4 December [O.S. 21 November] 1902) was a
    Russian bass opera singer and actor. He was the father of Igor Stravinsky and the
    grandfather of Soulima Stravinsky."""

    d = ed.extract(p)
    assert d[0] == None
    assert d[1] == None


def test_extract_borndate_in_sentence2():
    # https://en.wikipedia.org/wiki/Mikhail_Kruglov
    p = """Mikhail Kruglov (Russian: Михаил Круглов) is a Russian opera, folk and choir singer
    possessing a strong low-ranging oktavist voice.[1] Mr Kruglov was born in Siberia in
    1972."""
    d = ed.extract(p)
    assert d[0] == '1972-01-01'
    assert d[1] == None

# https://en.wikipedia.org/wiki/Stephen_Milling
# This one has the born date after the first paragraph. Under the Career section.

"""
Tests for is_integer(num)
"""


def test_isinteger_10_returnsTrue():
    assert ed.is_integer(10)


def test_isinteger_str10_returnsTrue():
    assert ed.is_integer('10')


def test_isinteger_string_returnsFalse():
    assert ed.is_integer('string') is False


def test_isinteger_float_returnsFalse():
    assert ed.is_integer(10.5) is False


def test_isinteger_str10pt3_returnsTrue():
    assert ed.is_integer('10.3') is False


"""
Tests for date_component(text):
"""


def test_datecomponent_10_returnsTrue():
    assert ed.date_component('10')


"""
Tests for scan_infoboxes(soup)
"""


def test_scaninfobox_vcard_borndate1():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/George_Andguladze')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1984-08-06'
    assert dday is None


def test_scaninfobox_vcard_borndate2():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Paata_Burchuladze')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1955-02-12'
    assert dday is None


def test_scaninfobox_vcard_bornyear():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/R%C3%BAni_Brattaberg')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1966-01-01'
    assert dday is None


def test_scaninfobox_vcard_bornyear_looksdifferent():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Deyan_Vatchkov')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1979-04-08'
    assert dday is None


def test_scaninfobox_vcard_bothdates():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Peter_Dyneley')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1921-04-13'
    assert dday == '1977-08-19'


def test_scaninfobox_vcard_justyear():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Harry_van_der_Kamp')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1947-01-01'
    assert dday is None


def test_extract_vcard_problem():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Giuseppina_Brambilla')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1819-05-09'
    assert dday == '1903-04-01'


def test_scaninfobox_plainlist():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Matthew_Stiff')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1979-12-13'
    assert dday is None


def test_scaninfobox_plainlist_bothdates():
    soup = scrapekit.handle_url('https://en.wikipedia.org/wiki/Martti_Talvela')
    bday, dday = ed.scan_infoboxes(soup)
    assert bday == '1935-02-04'
    assert dday == '1989-07-22'


"""
Tests for get_first_sentence(text):
"""


"""
Tests for extract_parens(text):
"""


"""
Tests for clean_initials(text):
"""


def test_cleaninitials_sentence():
    t = 'This is a sentence.'
    assert ed.clean_initials(t) == 'This is a sentence.'


def test_cleaninitials_endperiod():
    t = 'This is a SENTENCE.'
    assert ed.clean_initials(t) == t


def test_cleaninitials_name_with_lone_letter():
    t = 'Hors D\'oeuvre'
    assert ed.clean_initials(t) == 'Hors D\'oeuvre'


@pytest.mark.skip(reason="Beyond the scope of this problem.")
def test_cleaninitials_dr_title():
    t = 'Dr. Hooves'
    assert ed.clean_initials(t) == 'Dr Hooves'


def test_cleaninitials_1initial():
    t = 'James T. Kirk'
    assert ed.clean_initials(t) == 'James T Kirk'


def test_cleaninitials_2initials():
    t = 'Q. T. Prism'
    assert ed.clean_initials(t) == 'Q T Prism'


def test_cleaninitials_2initials_start():
    t = 'B.J. Hunnicutt'
    assert ed.clean_initials(t) == 'BJ Hunnicutt'


def test_cleaninitials_2abbrevs():
    t = 'Magnum, P.I.'
    assert ed.clean_initials(t) == 'Magnum, PI'
