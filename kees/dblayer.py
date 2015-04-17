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

def jsonisify(input):
	rs =  [x.__dict__ for x in input]
	for x in rs:
		for k,i in x.iteritems():
			print "obj: ",i, " key ",k
			if hasattr(i, 'isoformat'):
				print "DATE"
				x[k]=i.isoformat()
		try:
			del x['_sa_instance_state']
			#del x['created']
		except:
			pass

	return rs


def listProposals():
	#s=session()
	sqp = s.query(Post).all()
	return jsonisify(sqp)

def viewProposal(prop_id):
	sqp = s.query(Post).filter(Post.id==prop_id).all()
	return jsonisify(sqp)

def createProposal(sid, PropText):
	#s=session()
	ses = getsession(sid)
	if not ses:
		return False
	author = authorFromSes(ses)
	print author, PropText
	testpoint = Post(author=author, name=PropText, votenum=0)
	s.add(testpoint)
	s.commit()
	
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
