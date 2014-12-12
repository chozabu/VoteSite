import datetime, time
import dataset

#db = dataset.connect('sqlite:///:memory:')
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
def newAccount(username, password):
	username = username.replace(".","")
	usertable = db['users']
	#eUser = database.users.find_one({"_id":username})
	eUser = table.find_one(username=username)
	if(eUser):
		print "dupe account creation attempt on name: " + username
		return {"result":"fail", "message":"name taken"}
	newUser = {}
	newUser['createdAt'] = time.time()
	newUser['lastTouch'] = time.time()
	salt = newUser['salt'] = uuid.uuid4().get_hex()
	newUser['_id'] = username
	makeImage(username)
	newUser['username'] = username
	newUser['groups'] = []
	newUser['password'] = hashlib.sha512(password + salt.hexdigest())
	usertable.insert(newUser)
	#database.users.insert(newUser)
	print {"result":"sucess", "message":"account " + username + " created"}
	return {"result":"sucess", "message":"account " + username + " created"}