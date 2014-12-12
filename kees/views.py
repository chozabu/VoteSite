from pyramid.view import view_config

import os
import uuid
import string
import dblayer
from pyramid.response import Response


if not os.path.exists("ppsshots"):os.makedirs("kees/pplevels")
if not os.path.exists("crashs"):os.makedirs("kees/thumbs")

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

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
	return {'project': 'kees'}


#@view_config(route_name='home', renderer='json')
#def my_view(request):
#    return {"text":"hello"}

@view_config(route_name='uploadLevel', renderer='json')
def uploadLevel(request):
	i = request.POST
	'''print i
	print "POST uploading level"
	for item in i:
		print ""
		print "key", item
		print "item", i[item]
		#print "dir", dir(i[item])
		print "file", i[item].file.read()
		#print "filedir", dir(i[item].file)
		print "filename", i[item].filename'''
	#userResult = authUser(i)
	#print userResult
	#if userResult != True: return fail(userResult)
	author =  i['author'].file.read()
	name =  i['name'].file.read()
	leveldata = i['leveldata'].file
	sshot = i['sshot'].file

	fullname = pythonicVarName(author+name)

	namepath = "kees/pplevels/" + fullname
	write_a_file(namepath, leveldata)

	#import base64
	#ssdata = base64.b64decode(i.sshot)
	namepath = "kees/thumbs/" + fullname+".png"
	write_a_file(namepath, sshot)
	
	
	dblayer.add_level(name,author,fullname)
	return {"asdasd":"qweqwe"}
	return Response("OK")


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