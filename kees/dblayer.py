__author__ = 'chozabu'
import dataset
from OrmDefs import *
fp = 'mydatabase.sqlite'
# Remove the existing orm_in_detail.sqlite file
if os.path.exists(fp):
    os.remove(fp)

from sqlalchemy.sql import func
from sqlalchemy import create_engine
engine = create_engine('sqlite:///mydatabase.sqlite')
#db = dataset.connect('sqlite:///mydatabase.db')

from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

s = session()
#db


import datetime, time
import dataset
import uuid, hashlib

#db = dataset.connect('sqlite:///:memory:')
sessions = {}
#db = dataset.connect('sqlite:///mydatabase.db')

#v = VotePost(author=chozabu, post=testpoint,value=.5)

def jsonify_list(input):
	return [jsonify(x) for x in input]

def jsonify(input):
	#print "in ",input
	x=dict(input.__dict__)
	#print "x ",x
	for k,i in x.iteritems():
		#print "obj: ",i, " key ",k
		if hasattr(i, 'isoformat'):
			#print "DATE"
			x[k]=i.isoformat()
	try:
		del x['_sa_instance_state']
		#del x['created']
	except:
		pass
	try:
		del x['post_to']
	except:
		pass
	try:
		del x['post_from']
	except:
		pass

	return x

def jsonify_proposal(x):
		#print "prop ref: ", x.__dict__
		new=jsonify(x)
		#print "json proposal: ", new
		new['author']=x.author.name
		try:
			del new['connectionItems']
		except:
			pass
		try:
			del new['back_connectionItems']
		except:
			pass
		return new


def queryProposals(sortkey, start, count):
	sqp = s.query(Post).order_by(getattr(Post, sortkey))[start:count]
	#sqp = s.query(Post).filter().all()
	result = []
	for x in sqp:
		result.append(jsonify_proposal(x))
	return result

def listProposals():
	sqp = s.query(Post).all()
	result = []
	for x in sqp:
		result.append(jsonify_proposal(x))
	return result

def viewProposal(prop_id):
	x= s.query(Post).get(prop_id)
	return jsonify_proposal(x)

def getAllConnections_id(prop_id, clist={}):
	x= s.query(Post).get(prop_id)
	nodes, connections = getAllConnections(x)
	return {"nodes":nodes,"connections":[c for c in connections.values()]}
	#return [item for item in getAllConnections(x).iterkeys()]
def getAllConnections(prop, clist={}, plist={}):
	clist[prop.id]={"name": prop.name, "rating": prop.rating}
	for c in prop.connectionItems:
		if c not in plist:
			plist[c]={"type":c.type,"from":c.post_from_id,"to":c.post_to_id}
		if c.post_to.id not in clist:
			getAllConnections(c.post_to, clist,plist)
	for c in prop.back_connectionItems:
		if c not in plist:
			plist[c]={"type":c.type,"from":c.post_from_id,"to":c.post_to_id}
		if c.post_from.id not in clist:
			getAllConnections(c.post_from, clist,plist)
	return clist, plist

def getConnections(prop_id):
	c_from = []
	c_to = []
	x= s.query(Post).get(prop_id)
	for item in x.connectionItems:
		#print item
		nitem = jsonify(item)
		nitem['data']=jsonify_proposal(item.post_to)
		c_from.append(nitem)

	for item in x.back_connectionItems:
		nitem = jsonify(item)
		nitem['data']=jsonify_proposal(item.post_from)
		c_to.append(nitem)
	#print "Connection DATA: ", c
	return {"from":c_from,"to":c_to}

def createProposal(sid, PropText):
	print "creating prop, ", PropText
	#s=session()
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	#print "author: ", author.name
	testpoint = Post(author=author, name=PropText, votenum=0, rating=.0)
	#print "pointname", testpoint.name
	s.add(testpoint)
	s.commit()
	point = s.query(Post).get(testpoint.id)
	return jsonify_proposal(point)
	
def voteProposal(sid, prop_id, value):
	#s=session()
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	point = s.query(Post).get(prop_id)
	print "new vote of: ", value, " on ", point.name, " by ", author.name
	v = VotePost(author=author, post=point,value=value)

	s.add(v)
	s.commit()


	point.votenum+=1
	q= s.query(func.avg(VotePost.value).label('average')).filter(VotePost.post_id==point.id).one()
	print "new average:, ", q, " old average: ", point.rating
	point.rating=q[0]
	s.commit()
def joinProposal(sid, prop_id, prop_id2, cType):
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	point = s.query(Post).get(prop_id)
	point2 = s.query(Post).get(prop_id2)
	c = PostPostLink(post_from=point,post_to=point2,type=cType)
	s.add(c)
	s.commit()
def createComment(sid, prop_id, text, parent_id=None):
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	point = s.query(Post).get(prop_id)
	c = Comment(post_id=prop_id, text=text, author=author, parent_id=parent_id)
	s.add(c)
	s.commit()
	return c.id
def getsession(session):
	if sessions.has_key(session) == False:
		return False
	sRef = sessions[session]
	sRef['lastTouch'] = time.time()
	return sRef

def authorFromSes(sref):
	#s=session()
	result = s.query(Author).filter(Author.name == sref['username']).all()
	if len(result):
		return result[0]
	return None

def newSession(userRef):
	timeNow = time.time()
	session = {}
	session['_id'] = uuid.uuid4().get_hex()
	session['startTime'] = timeNow
	session['lastTouch'] = timeNow
	session['info'] = {}
	sessions[session['_id']] = session
	session['username'] = userRef.name
	session['id'] = userRef.id
	checkTimedOutSessions()
	return session

def checkTimedOutSessions():
	texpire = time.time()-1000*60*60#*24*7
	remsessions = []
	for sid in sessions:
		sRef = sessions[sid]
		if sRef['lastTouch'] < texpire:
			remsessions.append(sid)
			#sessions.pop(sid)
	for s in remsessions:
		sessions.pop(s)

def login(username, password):
	#s=session()
	username = username.replace(".","")
	#usertable = db['users']
	#eUser = usertable.find_one(username=username)
	sq = s.query(Author).filter(Author.name==username).all()
	#print "---", sq
	if len(sq):
		eUser = sq[0]
		#print eUser
		# makeImage(username)
		if hashlib.sha512(password + eUser.salt).hexdigest() == eUser.password:
			msession	 = newSession(eUser)
			#eUser.lastTouch = time.time()
			#usertable.update(eUser,['username'])
			returnInfo = {"result":"OK", "session":msession['_id'], "message":"logged in", "username":username, "_id":username}#, "noteCount":eUser['noteCount']}
			print returnInfo
			return returnInfo
		wrongpass = {"result":"fail", "message":"incorrect password"}
		print wrongpass
		return wrongpass
	wrongUser = {"result":"fail", "message":"user not found"}
	print wrongUser
	return wrongUser

def new_user(username, password):
	#s=session()
	username = username.replace(".","")
	
	sq = s.query(Author).filter(Author.name==username).all()
	if len(sq):
		print "dupe account creation attempt on name: " + username
		#return login(username, password)
		return {"result":"fail", "message":"name taken"}
	salt = uuid.uuid4().get_hex()
	newuser = Author(name=username, password = hashlib.sha512(password + salt).hexdigest(), salt=salt)
	s.add(newuser)
	s.commit()
	print {"result":"OK", "message":"account " + username + " created"}
	return {"result":"OK", "message":"account " + username + " created"}


new_user("Guest", "nopassword")
