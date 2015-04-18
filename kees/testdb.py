import dblayer

print "\n new user"
print dblayer.new_user("123", "456")

print "\n new user"
print dblayer.new_user("123", "456")

print "\n login user"
loginfo = dblayer.login("123", "456")
sid = loginfo['session']
print "\n create prop"
p1 = dblayer.createProposal(sid, "Improve this system")

#p1
p2 = dblayer.createProposal(sid, "Make GUI Nice")
p3 = dblayer.createProposal(sid, "Make Search function")
p4 = dblayer.createProposal(sid, "Make Connection OverView")
p1d = dblayer.createProposal(sid, "Make this system Distrubited")

#p2
p5 = dblayer.createProposal(sid, "Re-write FrontEnd")

#p3
p6 = dblayer.createProposal(sid, "Add good Query API")
#p4
p7 = dblayer.createProposal(sid, "Add API method with output close to d3")

print "\n list props"
print dblayer.listProposals()

props = dblayer.listProposals()
p1 = props[0]
p2 = props[1]

print "\n connect prop"
dblayer.joinProposal(sid, p2['id'], p1['id'], "leadsto")
dblayer.joinProposal(sid, p3['id'], p1['id'], "leadsto")
dblayer.joinProposal(sid, p4['id'], p1['id'], "leadsto")
dblayer.joinProposal(sid, p1d['id'], p1['id'], "leadsto")

dblayer.joinProposal(sid, p5['id'], p2['id'], "leadsto")

dblayer.joinProposal(sid, p6['id'], p3['id'], "leadsto")

dblayer.joinProposal(sid, p7['id'], p4['id'], "leadsto")

print "\n vote prop"
dblayer.voteProposal(sid, p1['id'], .9)
dblayer.voteProposal(sid, p1['id'], .5)
dblayer.voteProposal(sid, p2['id'], .1)
dblayer.voteProposal(sid, p3['id'], .2)
dblayer.voteProposal(sid, p4['id'], .99)
dblayer.voteProposal(sid, p5['id'], .01)
dblayer.voteProposal(sid, p6['id'], .23)
dblayer.voteProposal(sid, p7['id'], .76)
dblayer.voteProposal(sid, p1d['id'], .23)


print "\n list props"
print dblayer.listProposals()

print "\n connections"
#print dblayer.getConnections(p1['id'])
cdata = dblayer.getAllConnections_id(p1['id'])
for x in cdata:
	print x
	print cdata[x]

print "\n query"

sortedprops = dblayer.queryProposals("rating",0,8)
for p in sortedprops:
	print ""
	print p['rating'], p['name']
#print dblayer.getConnections(p2['id'])

print "\n comment"
comment1 = dblayer.createComment(sid, p1['id'], "Comment One")
print comment1
comment2 = dblayer.createComment(sid, p1['id'], "Comment Two")
print comment2
comment3 = dblayer.createComment(sid, p1['id'], "Comment ONE-REPLY", comment1)
print comment3

print "\n vote comment"
dblayer.voteComment(sid, comment1, .9)

