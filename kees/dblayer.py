__author__ = 'chozabu'
import dataset
from OrmDefs import *
fp = 'mydatabase.sqlite'
# Remove the existing orm_in_detail.sqlite file
if os.path.exists(fp):
    os.remove(fp)

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

def listProposals():
	#s=session()
	sqp = s.query(Post).all()
	return [x.__dict__ for x in sqp]

def viewProposal(prop_id):
	return [x.__dict__ for x in s.query(Post).filter(Post.id==prop_id).all()]

def createProposal(sid, PropText):
	#s=session()
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	print author
	#author = ses['username']
	testpoint = Post(author=author, name=PropText)
	s.add(testpoint)
	s.commit()
	
def voteProposal(sid, prop_id, value):
	#s=session()
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	point = s.query(Post).get(prop_id)
	v = VotePost(author=author, post=point,value=value)
	s.add(v)
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
