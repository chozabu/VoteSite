from pyramid.view import view_config

import os
import uuid
import string
import dblayer
import datetime
from pyramid.response import Response


if not os.path.exists("kees/pplevels"):os.makedirs("kees/pplevels")
if not os.path.exists("kees/thumbs"):os.makedirs("kees/thumbs")
if not os.path.exists("kees/crashs"):os.makedirs("kees/crashs")

def pythonicVarName(field):
	firstLetter = True
	for word in field.split(' '):
		if firstLetter == False:
			wordCapped = str(word[0]).upper() + word[1:]
			id = id + wordCapped
		else:
			id = word.lower()
		firstLetter = False
	for i in string.punctuation:
		if i in id:
			id = id.replace(i, "")
	return id

def write_a_file(file_path, input_file):
	temp_file_path = file_path + '~'
	output_file = open(temp_file_path, 'wb')

	# Finally write the data to a temporary file
	input_file.seek(0)
	while True:
		data = input_file.read(2<<16)
		if not data:
			break
		output_file.write(data)

	# If your data is really critical you may want to force it to disk first
	# using output_file.flush(); os.fsync(output_file.fileno())

	output_file.close()

	# Now that we know the file has been fully saved to disk move it into place.

	os.rename(temp_file_path, file_path)
def write_some_data(file_path, input_data):
	temp_file_path = file_path + '~'
	output_file = open(temp_file_path, 'wb')

	# Finally write the data to a temporary file
	output_file.write(input_data)

	# If your data is really critical you may want to force it to disk first
	# using output_file.flush(); os.fsync(output_file.fileno())

	output_file.close()

	# Now that we know the file has been fully saved to disk move it into place.

	os.rename(temp_file_path, file_path)

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
	return {'project': 'kees'}


#@view_config(route_name='home', renderer='json')
#def my_view(request):
#    return {"text":"hello"}

@view_config(route_name='new_user', renderer='json')
def new_user(request):
	i = request.POST
	username =  i['username']
	print username
	password =  i['password']
	return dblayer.new_user(username,password)
@view_config(route_name='login', renderer='json')
def login(request):
	i = request.POST
	username =  i['username']
	password =  i['password']
	return dblayer.login(username,password)

@view_config(route_name='complex_query_levels', renderer='json')
def complex_query_levels(request):
	i = request.POST
	'''sortKey =  str(i['sortKey'])
	cursor =  int(i['cursor'])
	limit =  int(i['limit'])'''
	levels = dblayer.complex_query_levels()
	#return Response("OK")
	return levels

@view_config(route_name='query_levels', renderer='json')
def query_levels(request):
	i = request.POST
	sortKey =  str(i['sortKey'])
	cursor =  int(i['cursor'])
	limit =  int(i['limit'])
	levels = dblayer.query_levels(sortKey,cursor,limit)
	#return Response("OK")
	return levels

@view_config(route_name='query_points', renderer='json')
def query_points(request):
	print "points"
	i = request.POST
	sortKey =  str(i['sortKey'])
	cursor =  int(i['cursor'])
	limit =  int(i['limit'])
	points = dblayer.query_points(sortKey,cursor,limit)
	print points
	return points

@view_config(route_name='get_tags', renderer='json')
def get_tags(request):
	print "TAGS"
	i = request.POST
	print i
	docid =  i['id']
	print "requesting: ", docid
	tags = dblayer.get_tags(docid)
	print tags
	return tags

@view_config(route_name='get_point', renderer='json')
def get_point(request):
	print "HELLO"
	i = request.POST
	print i
	docid =  i['id']
	dbid =  'points'#i['dbid']
	print "docid=",docid
	point = dblayer.get_one(dbid, uid=docid)
	print point
	return point

@view_config(route_name='get_level', renderer='json')
def get_level(request):
	print "HELLO"
	i = request.POST
	print i
	docid =  i['id']
	dbid =  'pplevels'#i['dbid']
	print "docid=",docid
	point = dblayer.get_one(dbid, uid=docid)
	print point
	return point

@view_config(route_name='add_vote', renderer='json')
def add_vote(request):
	i = request.POST
	print i
	dbid =  str(i['dbid'])
	print dbid
	if dbid not in ['points', 'pplevels']:
		print "db not accepted"
		return {"status":"fail"}
	print "db accepted"
	session =  str(i['session'])
	print "session=", session
	val =  float(i['val'])
	print "val=", val
	docid =  str(i['docid'])
	print "docid=", docid
	tag = i.get('tag', None)

	return dblayer.add_vote(session,val,docid,dbid,tag=tag)

@view_config(route_name='add_point', renderer='json')
def add_point(request):
	i = request.POST
	session =  i['session']
	print session
	name =  i['name']
	text =  i['text']
	return dblayer.add_point(session, name, text)

@view_config(route_name='uploadLevel', renderer='json')
def uploadLevel(request):
	i = request.POST
	session =  i['session'].file.read()
	print session
	author =  i['author'].file.read()
	name =  i['name'].file.read()
	leveldata = i['leveldata'].file
	sshot = i['sshot'].file
	fullname = pythonicVarName(author+name)
	tags = i.get("tags_str").file.read()
	if dblayer.add_level(session, name, author, fullname, tags):


		namepath = "kees/pplevels/" + fullname
		write_a_file(namepath, leveldata)

		namepath = "kees/thumbs/" + fullname+".png"
		write_a_file(namepath, sshot)

		return {"result":"OK"}
	return {"result":"FAIL","dta":[session,author,name], "insessions":session in dblayer.sessions}
	#return Response("OK")



@view_config(route_name='uploadCrash', renderer='json')
def uploadCrash(request):
	i = request.POST
	print "POST uploading crash"

	now = str(datetime.datetime.now())
	crashData = i['crashData']

	namepath = "kees/crashs/" + now+"--" + str(i['version'])
	write_some_data(namepath, crashData)

	return {"result":"OK"}

@view_config(route_name='crashLogs', renderer='json')
def crashLogs(request):
		files = os.listdir('kees/crashs')
		#result = "".join('<a href="crashs/'+f+'" </>'+f+'</a><br/>' for f in files)
		result = "".join('<a href="kees/crashs/'+f+'" </>'+f+'</a><br/>' for f in files)
		return Response(body=result,headerlist=[('Content-Type', 'text/html')])


@view_config(route_name='store_mp3_view', renderer='json')
def store_mp3_view(request):
	# ``filename`` contains the name of the file in string format.
	#
	# WARNING: this example does not deal with the fact that IE sends an
	# absolute file *path* as the filename.  This example is naive; it
	# trusts user input.

	filename = request.POST['mp3'].filename

	# ``input_file`` contains the actual file data which needs to be
	# stored somewhere.

	input_file = request.POST['mp3'].file

	# Note that we are generating our own filename instead of trusting
	# the incoming filename since that might result in insecure paths.
	# Please note that in a real application you would not use /tmp,
	# and if you write to an untrusted location you will need to do
	# some extra work to prevent symlink attacks.

	file_path = os.path.join('/tmp', '%s.mp3' % uuid.uuid4())

	# We first write to a temporary file to prevent incomplete files from
	# being used.

	temp_file_path = file_path + '~'
	output_file = open(temp_file_path, 'wb')

	# Finally write the data to a temporary file
	input_file.seek(0)
	while True:
		data = input_file.read(2<<16)
		if not data:
			break
		output_file.write(data)

	# If your data is really critical you may want to force it to disk first
	# using output_file.flush(); os.fsync(output_file.fileno())

	output_file.close()

	# Now that we know the file has been fully saved to disk move it into place.

	os.rename(temp_file_path, file_path)

	return Response('OK')