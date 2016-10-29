# coding=utf-8
import opera_singers as wos

"""
Tests for the functions in wikipedia_opera_singers.py
"""


"""
Tests for parse_voicetype(url):
"""


def test_parsevoicetype_Operatic_bass_baritones():
    u = 'https://en.wikipedia.org/wiki/Category:Operatic_bass-baritones'
    v = wos.parse_voicetype(u)
    assert v == 'Operatic bass-baritones'


def test_parsevoicetype_Operatic_basses():
    u = 'https://en.wikipedia.org/wiki/Category:Operatic_basses'
    v = wos.parse_voicetype(u)
    assert v == 'Operatic basses'


def test_parsevoicetype_Operatic_castrati():
    u = 'https://en.wikipedia.org/wiki/Category:Castrati'
    v = wos.parse_voicetype(u)
    assert v == 'Castrati'


"""
Tests for parse_name(url):
"""


def test_parsename_firstlast():
    n = wos.parse_name('https://en.wikipedia.org/wiki/Adamo_Didur')
    assert n[0] == 'Adamo'
    assert n[-1] == 'Didur'


def test_parsename_firstlast_parens():
    n = wos.parse_name('https://en.wikipedia.org/wiki/Norman_Foster_(bass)')
    assert n[0] == 'Norman'
    assert n[-1] == 'Foster'


def test_parsename_firstlast_foreignchar():
    n = wos.parse_name('https://en.wikipedia.org/wiki/Jean-Fran%C3%A7ois_Delmas_(bass-baritone)')
    assert n[0] == "Jean-Fran%C3%A7ois"
    assert n[-1] == 'Delmas'


def test_parsename_firstmidlast():
    n = wos.parse_name('https://en.wikipedia.org/wiki/Kenneth_Lee_Spencer')
    assert n[0] == 'Kenneth'
    assert n[-1] == 'Spencer'
