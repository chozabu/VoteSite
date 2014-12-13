__author__ = 'chozabu'
from random import random
import dblayer
import uuid

us1 = "choza"
us2 = "qweas"

print dblayer.new_user(us1, "asd")
print ""
session = dblayer.login(us1, "asd")['session']
print session

lvls = dblayer.query_levels("filename")
print lvls

l0 = lvls[0]['uid']
print l0

#dblayer.add_vote(session,.8,'pplevels', l0)
dblayer.add_vote(session,.3,'pplevels', l0)


print dblayer.new_user(us2, "asd")
print ""
session = dblayer.login(us2, "asd")['session']
dblayer.add_vote(session,.9,'pplevels', l0)
'''print dblayer.new_user(us1, "asd")
print dblayer.new_user(us2, "asd")


print dblayer.login(us1, "asd")

pplevels = dblayer.db['pplevels']
ppl = []
for x in pplevels:
	ppl.append(x)
for x in ppl:
	uid = uuid.uuid4().get_hex()
	pplevels.update(dict(id=x['id'], uid=uid), ['id'])
	

pplevels = dblayer.db['pplevels']
for x in pplevels:
	print x
'''