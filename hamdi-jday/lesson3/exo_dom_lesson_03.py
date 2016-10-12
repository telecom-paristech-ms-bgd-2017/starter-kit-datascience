from urllib.request import urlopen
from lxml.html import parse
from pandas.io.parsers import TextParser


url = 'https://gist.github.com/paulmillr/2657075'
parsed = parse(urlopen(url))
doc = parsed.getroot()
tables = doc.findall('.//table')
rows = tables[0].findall('.//tr')


def _unpack(row, kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text_content() for val in elts]


header = _unpack(rows[0], kind='th')
data = [_unpack(r) for r in rows[1:]]
clean_data = TextParser(data, names=header[1:]).get_chunk()
clean_data.to_csv('256_Top_Contributors.csv')
print('List of 256 Top contributors saved in 256_Top_Contributors.csv')
