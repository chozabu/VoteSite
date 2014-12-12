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

def add_level(name, author, fullname):
	isNew = True
	levelstable = db['pplevels']
	record = levelstable.find_one(filename=fullname)
	print record, record==None
	if record != None:
		isNew = False
		print "not new"
	else:
		print "new"
	newLevel = {}
	newLevel['name'] = name
	newLevel['author'] = author
	newLevel['filename'] = fullname
	now = str(datetime.datetime.now())
	nowStamp = time.time()
	if (isNew):
		newLevel['rating'] = .5
		newLevel['ratingCount'] = 0
		newLevel['dateAdded'] = nowStamp
		newLevel['downloads'] = 0
	newLevel['dateModified'] = nowStamp
	newLevel['description'] = "description"
	newLevel['screenshot'] = "none"
	#db.ppLevels[fullname] = newLevel
	if isNew:
		levelstable.insert(newLevel)
	else:
		levelstable.update(newLevel,['filename'])
def query_levels(sortKey, cursor=0, limit=8, **_filter):
	levelstable = db['pplevels']
	a= levelstable.find(_limit=limit, _offset=cursor, order_by=sortKey, **_filter)
	return a

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
	texpire = time.time()-1000*60*60
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
			returnInfo = {"result":"sucess", "session":session['_id'], "message":"logged in", "username":username, "_id":username, "noteCount":eUser['noteCount']}
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
	print {"result":"sucess", "message":"account " + username + " created"}
	print usertable.find_one(username=username)
	return {"result":"sucess", "message":"account " + username + " created"}