import datetime, time
import dataset
import uuid, hashlib

#db = dataset.connect('sqlite:///:memory:')
sessions = {}
db = dataset.connect('sqlite:///mydatabase.db')
'''database=db

table = db['sometable']
table.insert(dict(name='John Doe', age=37))
table.insert(dict(name='Jane Doe', age=34, gender='female'))

john = table.find_one(name='John Doe')

print john
'''

def add_vote(session, val, docid, dbid='pplevels', tag=None):
	sRef = getsession(session)
	if not sRef:
		return False
	levelstable = db[dbid]
	record = levelstable.find_one(uid=docid)
	print record, record==None
	if record == None:
		return {'result':'fail', 'reason':'voteable item not found'}
	username = sRef['username']

	istag = tag!=None

	votes_stable = db['votes']
	# votes_meta_table = db['votes_meta']
	# vote_meta = votes_meta_table.find_one(docid=docid)
	# if not vote_meta:
	# 	vote_meta = dict(docid=docid, votenum=1, rating=val, heat=1.)
	# else:
	if not istag:
		votenum=record['ratingCount']
		rating=record['rating']
		print "RATING working directly on record"
	else:
		print "TAG - working on meta"
		votes_group_table = db['vote_groups']
		vote_group = votes_group_table.find_one(dbid=dbid, docid=docid, tag=tag)
		if not vote_group:
			vote_group = new_vote_group(docid=docid, dbid=dbid, tag=tag)
		votenum=vote_group['ratingCount']
		rating=vote_group['rating']
	print "Rating was, ", rating
	print username,docid
	vote = votes_stable.find_one(user=username, docid=docid)
	print "-------------"
	print "vote=",vote
	print "val=", val
	print ""
	if not vote:
		vp1=float(votenum+1.)
		print "vp1=",vp1
		rating=rating/vp1*votenum+val/(vp1)
		votenum=vp1
		print "new vote, rating now, ", rating
	else:
		oldval=vote['value']
		print oldval, votenum
		if votenum<1:
			rating=val
		else:
			rating=rating-oldval/votenum+val/votenum
		print "re-vote, rating now, ", rating

	if not istag:
		vote_meta = dict(uid=docid, ratingCount=votenum, rating=rating)
		levelstable.update(vote_meta,['uid'])
	else:
		vote_group['ratingCount']=votenum
		vote_group['rating']=rating
		votes_group_table.upsert(vote_group, ['uid'])

	newVote = {"user":username, "value":val, "time":time.time(), "docid":docid}
	votes_stable.upsert(newVote,['user', 'docid'])
	print "xoxoxoxoxoxoxoxoxoxoxox"
	return True

def get_tags(docid):
	votes_group_table = db['vote_groups']
	rawtags = votes_group_table.find(docid=docid)
	tags = [x for x in rawtags]
	print "tags=", tags
	return tags

def new_voteable(name, author):
	newLevel = {}
	newLevel['uid'] = uuid.uuid4().get_hex()
	newLevel['name'] = name
	newLevel['author'] = author
	nowStamp = time.time()
	newLevel['rating'] = .5
	newLevel['ratingCount'] = 0
	newLevel['dateAdded'] = nowStamp
	newLevel['dateModified'] = nowStamp
	return newLevel

def new_vote_group(docid, dbid, tag):
	newLevel = {}
	newLevel['uid'] = uuid.uuid4().get_hex()
	newLevel['docid'] = docid
	newLevel['dbid'] = dbid
	newLevel['tag'] = tag
	nowStamp = time.time()
	newLevel['rating'] = .5
	newLevel['ratingCount'] = 0
	newLevel['dateAdded'] = nowStamp
	newLevel['dateModified'] = nowStamp
	return newLevel

def add_level(session, name, author, fullname, tags_str=None, tags=[]):
	ses = getsession(session)
	if not ses:
		return False
	isNew = True
	levelstable = db['pplevels']
	record = levelstable.find_one(filename=fullname)
	print record, record==None
	if record != None:
		isNew = False
		print "not new"
	else:
		print "new"
	if (isNew):
		record = new_voteable(name,author)
		record['filename'] = fullname
		record['downloads'] = 0
	else:
		nowStamp = time.time()
		record['dateModified'] = nowStamp
	record['description'] = "description"
	#db.ppLevels[fullname] = newLevel
	levelstable.upsert(record,['filename'])
	if tags_str:
		tags = tags_str.split()
	if tags:
		for t in tags:
			add_vote(session, 1, fullname, 'pplevels', tag=t)
	return True

def add_point(session, name, text):
	ses = getsession(session)
	if not ses:
		return False
	author = ses['username']
	isNew = True
	levelstable = db['points']
	#record = levelstable.find_one(filename=fullname)
	record = new_voteable(name,author)
	#record['filename'] = fullname
	#record['downloads'] = 0
	record['text'] = text
	#db.ppLevels[fullname] = newLevel
	levelstable.insert(record)
	return record
def query_levels(sortKey, cursor=0, limit=8, **_filter):
	levelstable = db['pplevels']
	print limit, cursor, sortKey
	a= levelstable.find(_limit=limit, _offset=cursor, order_by=sortKey, **_filter)
	return [x for x in a]
def query_points(sortKey, cursor=0, limit=8, **_filter):
	levelstable = db['points']
	print limit, cursor, sortKey
	a= levelstable.find(_limit=limit, _offset=cursor, order_by=sortKey, **_filter)
	return [x for x in a]
def get_one(dbid, **_filter):
	print "get_one"
	print dbid
	levelstable = db[dbid]
	print levelstable
	a= levelstable.find_one(**_filter)
	print a
	return a

def getsession(session):
	if sessions.has_key(session) == False:
		return False
	sRef = sessions[session]
	sRef['lastTouch'] = time.time()
	return sRef

def newSession(username, userRef):
	timeNow = time.time()
	session = {}
	session['_id'] = uuid.uuid4().get_hex()
	session['startTime'] = timeNow
	session['lastTouch'] = timeNow
	session['info'] = {}
	sessions[session['_id']] = session
	session['username'] = username
	# TODO CHECK FOR TIMED OUT SESSIONS elsewhere
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
	username = username.replace(".","")
	usertable = db['users']
	eUser = usertable.find_one(username=username)
	if(eUser):
		# makeImage(username)
		if hashlib.sha512(password + eUser['salt']).hexdigest() == eUser['password']:
			session	 = newSession(username, eUser)
			eUser['lastTouch'] = time.time()
			usertable.update(eUser,['username'])
			returnInfo = {"result":"OK", "session":session['_id'], "message":"logged in", "username":username, "_id":username, "noteCount":eUser['noteCount']}
			print returnInfo
			return returnInfo
		wrongpass = {"result":"fail", "message":"incorrect password"}
		print wrongpass
		return wrongpass
	wrongUser = {"result":"fail", "message":"user not found"}
	print wrongUser
	return wrongUser

def new_user(username, password):
	username = username.replace(".","")
	usertable = db['users']
	#eUser = database.users.find_one({"_id":username})
	eUser = usertable.find_one(username=username)
	print eUser
	if(eUser):
		print "dupe account creation attempt on name: " + username
		return login(username, password)
		return {"result":"fail", "message":"name taken"}
	newUser = {}
	newUser['createdAt'] = time.time()
	newUser['lastTouch'] = time.time()
	salt = newUser['salt'] = uuid.uuid4().get_hex()
	#newUser['_id'] = username
	#makeImage(username)
	newUser['username'] = username
	newUser['noteCount'] = 0
	#newUser['groups'] = []
	newUser['password'] = hashlib.sha512(password + salt).hexdigest()
	usertable.insert(newUser)
	#database.users.insert(newUser)
	print {"result":"OK", "message":"account " + username + " created"}