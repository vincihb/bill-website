from tool.Pickler import Pickler
from api.propublica.PropublicaScraper import PropublicaScraper
from os import path
from db.SqlExecutor import SqlExecutor

p = Pickler()
scrapper = PropublicaScraper()
local_dir = path.dirname(path.abspath(__file__))
OBJECT_PATH = path.join(local_dir, '..', '..', 'obj', 'complete', 'House Members.pkl')

members = p.load_obj(OBJECT_PATH)
print(len(members.keys()))
print(members.keys())
print(members['A000022'].keys())
print(members['A000022'])

OBJECT_PATH = path.join(local_dir, '..', '..', 'obj', 'complete', 'Senate Members.pkl')

members = p.load_obj(OBJECT_PATH)
print(len(members.keys()))
print(members.keys())
print(members['A000062'].keys())
print(members['A000062'])
exit()
