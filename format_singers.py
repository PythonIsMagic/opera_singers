import lxml.etree as etree
import scrapekit
from opera_singers import Singer
"""
  " Manages the XML creation for singer data.
  """

FILENAME = 'data/singers.xml'


def dummydata():
    """ Just some sample data to test with. """
    s1 = Singer('Ekkehard', 'Abele', 'Operatic bass-baritone', 'Unknown', 'n/a', 'n/a')
    s2 = Singer('Theo', 'Adam', 'Operatic bass-baritone', '1 August 1926', 'n/a', 'n/a')
    return [s1, s2]


def make_xml(filename, singers):
    """ Creates the actual XML file from the singer data."""
    root = etree.Element('root')
    doc = etree.SubElement(root, 'doc')

    for s in singers:
        if s is None:
            continue
        singer = etree.SubElement(doc, 'singer')

        for field, v in zip(Singer._fields, s):
            if v is None:
                v = 'n/a'
            element = etree.SubElement(singer, field)
            element.text = v
        """
        firstname = etree.SubElement(singer, 'singer')
        firstname.text = s.firstname

        lastname = etree.SubElement(singer, 'singer')
        lastname.text = s.lastname

        voicetype = etree.SubElement(singer, 'singer')
        voicetype.text = s.voicetype

        birthdate = etree.SubElement(singer, 'singer')
        birthdate.text = s.birthdate

        deathdate = etree.SubElement(singer, 'singer')
        deathdate.text = s.deathdate

        url = etree.SubElement(singer, 'singer')
        url.text = s.url
        """
        #  singer.set("firstname", s.firstname)
        # We don't need to do these singly...
        #  for field, v in zip(Singer._fields, s):
            #  v = (v if v else 'n/a')
            #  singer.set(field, v)

    text = etree.tostring(root, pretty_print=True)
    print(text)

    scrapekit.ensure_dir('data/')
    with open(filename, 'w') as f:
        f.write(text)


if __name__ == "__main__":
    data = dummydata()
    make_xml(FILENAME, data)
