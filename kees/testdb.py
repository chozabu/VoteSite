import dblayer

print "\n new user"
print dblayer.new_user("123", "456")

print "\n new user"
print dblayer.new_user("123", "456")

print "\n login user"
loginfo = dblayer.login("123", "456")

print "\n create prop"
p1 = dblayer.createProposal(loginfo['session'], "Improve this system")

#p1
p2 = dblayer.createProposal(loginfo['session'], "Make GUI Nice")
p3 = dblayer.createProposal(loginfo['session'], "Make Search function")
p4 = dblayer.createProposal(loginfo['session'], "Make Connection OverView")
p1d = dblayer.createProposal(loginfo['session'], "Make this system Distrubited")

#p2
p5 = dblayer.createProposal(loginfo['session'], "Re-write FrontEnd")

#p3
p6 = dblayer.createProposal(loginfo['session'], "Add good Query API")
#p4
p7 = dblayer.createProposal(loginfo['session'], "Add API method with output close to d3")

print "\n list props"
print dblayer.listProposals()

props = dblayer.listProposals()
p1 = props[0]
p2 = props[1]

print "\n connect prop"
dblayer.joinProposal(loginfo['session'], p2['id'], p1['id'], "leadsto")
dblayer.joinProposal(loginfo['session'], p3['id'], p1['id'], "leadsto")
dblayer.joinProposal(loginfo['session'], p4['id'], p1['id'], "leadsto")
dblayer.joinProposal(loginfo['session'], p1d['id'], p1['id'], "leadsto")

dblayer.joinProposal(loginfo['session'], p5['id'], p2['id'], "leadsto")

dblayer.joinProposal(loginfo['session'], p6['id'], p3['id'], "leadsto")

dblayer.joinProposal(loginfo['session'], p7['id'], p4['id'], "leadsto")

print "\n vote prop"
dblayer.voteProposal(loginfo['session'], p1['id'], .9)
dblayer.voteProposal(loginfo['session'], p1['id'], .5)


print "\n list props"
print dblayer.listProposals()

print "\n connections"
#print dblayer.getConnections(p1['id'])
cdata = dblayer.getAllConnections_id(p1['id'])
for x in cdata:
	print x
	print cdata[x]
#print dblayer.getConnections(p2['id'])