 
import dataset

#db = dataset.connect('sqlite:///:memory:')
db = dataset.connect('sqlite:///mydatabase.db')

table = db['sometable']
table.insert(dict(name='John Doe', age=37))
table.insert(dict(name='Jane Doe', age=34, gender='female'))

john = table.find_one(name='John Doe')

print john

def newAccount(request, username, password):
	username = username.replace(".","")
	eUser = database.users.find_one({"_id":username})
	if(eUser):
		print "dupe account creation attempt on name: " + username
		return {"result":"fail", "message":"name taken"}
	newUser = {}
	newUser['createdAt'] = time.time()
	newUser['lastTouch'] = time.time()
	newUser['salt'] = uuid.uuid4().get_hex()
	newUser['_id'] = username
	makeImage(username)
	newUser['username'] = username
	newUser['groups'] = []
	newUser['password'] = hashlib.sha512(password + newUser['salt']).hexdigest()
	database.users.insert(newUser)
	print {"result":"sucess", "message":"account " + username + " created"}
	return {"result":"sucess", "message":"account " + username + " created"}