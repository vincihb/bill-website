from tool.Pickler import Pickler
from api.PropublicaScraper import PropublicaScraper
from os import path

p = Pickler()
scrapper = PropublicaScraper()
local_dir = path.dirname(path.abspath(__file__))
OBJECT_PATH = path.join(local_dir, '..', '..', 'obj', 'complete', 'Bill Set-116-Complete.pkl')

bill = p.load_obj(OBJECT_PATH)
print(bill.keys())
print(bill['s1636-116'].keys())
print(bill['s1636-116'])
exit()
