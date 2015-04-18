This is currently a very simple voting server, forked from KivEntEds server.  
  
The plan is to have an abstract voting system, that can apply to any item in any table of the database.  
  
Some basic types will be:  
-Point  
-Connection 
-Tag  
  
All voteable of course.  

An Early interface should be a ZoomableUI displaying a point and all the ones it is connected to, and the ones they are connected  to, going onwards - perhaps to a recursion limit.  
  
A points dependant points will be below it.  
Higher ranked points will be to the left.  
  
This should quickly give an impression of a points popularity, and accuracy  
  
To test:
python runit.py

Or to test with some sample data:
cd kees; python testdb.py; cd .. ; python runit.py
firefox http://localhost:8080/static/graphpoint.html?id=2

API Refrence:

{'new_user', {username:'something', password;'pass'}},
returns
{"result":"OK", "message":"account " + username + " created"}

{'login', {username:'something', password;'pass'}},
returns
 {"result":"OK", "session":msession['_id'], "message":"logged in", "username":username, "_id":username}
sessionID=session





{'get_points', {}},
returns all points


{'get_point', {docid;'somedocid'}},
returns a point in detail


{'add_point', {session: sessionID, text:text.value}}

{'join_points', {session: sessionID, a: 'somedocid', b: 'somedocid', type:'connectiontype'}}


{'add_vote', {session: sessionID, val:0.0-1.0, docid;'somedocid'}},


  
Depends:  
sudo pip install paste  
sudo pip install PasteDeploy  
sudo pip install waitress  
sudo pip install pyramid  
sudo pip install pyramid_debugtoolbar  
sudo pip install pyramid_chameleon  
sudo pip install dataset  
