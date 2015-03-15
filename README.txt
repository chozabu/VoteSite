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

Depends:
pip install paste