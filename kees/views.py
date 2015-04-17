from pyramid.view import view_config

import os
import uuid
import string
import dblayer
import datetime
from pyramid.response import Response

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



	i = request.POST
	sortKey =  str(i['sortKey'])
	cursor =  int(i['cursor'])
	limit =  int(i['limit'])
	levels = dblayer.query_levels(sortKey,cursor,limit)
	#return Response("OK")
	return levels

@view_config(route_name='get_points', renderer='json')
def get_points(request):
	print "points"
	#i = request.POST
	#sortKey =  str(i['sortKey'])
	#cursor =  int(i['cursor'])
	#limit =  int(i['limit'])
	#print "querying", sortKey,cursor,limit
	points =dblayer.listProposals()
	print "returning, ", points
	return points
@view_config(route_name='get_point', renderer='json')
def get_point(request):
	print "points"
	#i = request.POST
	docid = str(i['docid'])
	#cursor =  int(i['cursor'])
	#limit =  int(i['limit'])
	#print "querying", sortKey,cursor,limit
	points =dblayer.listProposals()
	print "returning, ", points
	return points
@view_config(route_name='join_points', renderer='json')
def join_points(request):
	print "join"
	#i = request.POST
	cType =  str(i['type'])
	a =  int(i['a'])
	b =  int(i['b'])
	session =  i['session']
	#print "querying", sortKey,cursor,limit
	return dblayer.joinProposal(session, a,b,cType)

'''@view_config(route_name='query_points', renderer='json')
def query_points(request):
	print "points"
	i = request.POST
	sortKey =  str(i['sortKey'])
	cursor =  int(i['cursor'])
	limit =  int(i['limit'])
	print "querying", sortKey,cursor,limit
	points = dblayer.query_points(sortKey,cursor,limit)
	print "returning, ", points
	return points

	print "TAGS"
	i = request.POST
	print i
	docid =  i['id']
	print "requesting: ", docid
	tags = dblayer.get_tags(docid)
	print tags
	return tags'''

'''@view_config(route_name='get_point', renderer='json')
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

	print "HELLO"
	i = request.POST
	print i
	docid =  i['id']
	dbid =  'pplevels'#i['dbid']
	print "docid=",docid
	point = dblayer.get_one(dbid, uid=docid)
	print point
	return point'''

@view_config(route_name='add_vote', renderer='json')
def add_vote(request):
	i = request.POST
	print i
	session =  str(i['session'])
	print "session=", session
	val =  float(i['val'])
	print "val=", val
	docid =  str(i['docid'])
	print "docid=", docid
	return dblayer.voteProposal(session, docid, val)

@view_config(route_name='add_point', renderer='json')
def add_point(request):
	i = request.POST
	session =  i['session']
	print session
	text =  i['text']
	return dblayer.createProposal(session, text)
