__author__ = 'chozabu'
from random import random
import dblayer

us1 = "choz"+str(random())
us2 = "qwe"+str(random())

print dblayer.new_user(us1, "asd")
print dblayer.new_user(us1, "asd")
print dblayer.new_user(us2, "asd")


print dblayer.login(us1, "asd")
print dblayer.login(us1, "asd")
