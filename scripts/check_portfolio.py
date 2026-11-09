"""Check static links and consistency of the published HTML and project catalogue."""
import json
from pathlib import Path
from urllib.parse import urlsplit

from lxml import html

root = Path(__file__).resolve().parents[1]
source = (root / 'index.html').read_text(encoding='utf-8')
data = json.loads((root / 'showcase-data.json').read_text(encoding='utf-8'))
tree = html.fromstring(source)
text = ' '.join(' '.join(tree.itertext()).split())

def by_class(name):
    return tree.xpath(f"//*[contains(concat(' ', normalize-space(@class), ' '), ' {name} ')]")

assert len(by_class('case')) == len(data['projects']) == 5
assert len(by_class('library-row')) == len(data['library']) == 17
assert data['contact']['email'] == 'volckovna@gmail.com'
assert tree.xpath('//a[@href="mailto:volckovna@gmail.com"]')
assert not any(word in source.lower() for word in ['vanavany7', 'участвовал', 'дорабатывал', 'не завершён', 'требует исправления'])
for metric in ['15 048', '2 068', '14 038', '83', '90 000']:
    assert metric in text, metric
for project in data['projects']:
    assert project['name'] in text
    assert ' '.join(project['presentation']['contribution'].split()) in text, project['name']
for project in data['library']:
    assert project['name'] in text
    assert ' '.join(project['description'].split()) in text, project['name']
ids = set(tree.xpath('//@id'))
checked = 0
for reference in tree.xpath('//@href | //@src'):
    if reference.startswith(('http:', 'https:', 'mailto:', 'data:')):
        continue
    if reference.startswith('#'):
        assert reference[1:] in ids, reference
    else:
        assert (root / urlsplit(reference).path).is_file(), reference
    checked += 1
for target in data['resume']['formats'].values():
    assert (root / target).stat().st_size > 10000, target
print(json.dumps({'cases':5,'library':17,'local_links_checked':checked,'catalogue_matches_html':True,'email':'volckovna@gmail.com'}))
