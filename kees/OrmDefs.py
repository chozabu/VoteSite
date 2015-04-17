__author__ = 'chozabu'

import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased


Base = declarative_base()

#Author
#Post
#Post-Post Connection
#Vote (Posts, and more?)
#votegroup?
#VoteConnection?
#LiquidDelegation?
#Catagory?
#Tag?

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    name = Column(String)
    password = Column(String)
    salt = Column(String)
class PostPostLink(Base):
    __tablename__ = 'post_post_link'
    #id = Column(Integer, primary_key=True)
    type = Column(String)
    post_from_id = Column(ForeignKey('post.id'), primary_key=True)
    post_to_id = Column(ForeignKey('post.id'), primary_key=True)
    post_from = relationship(
        'Post',
		primaryjoin='PostPostLink.post_from_id==Post.id',
		backref=backref("connectionItems")
    )
    post_to = relationship(
        'Post',
		primaryjoin='PostPostLink.post_to_id==Post.id',
		backref=backref("back_connectionItems")
    )
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer)
    rating = Column(Float)
    created = Column(DateTime, default=func.now())
    name = Column(String)
    connections = relationship(
        'Post',
        secondary="post_post_link",
		primaryjoin=PostPostLink.post_from_id==id,
		secondaryjoin=PostPostLink.post_to_id==id,
		backref=backref("back_connections")
    )
    '''connectionItems = relationship(
        'PostPostLink',
        secondary="post_post_link",
		primaryjoin=PostPostLink.post_from_id==id,
		secondaryjoin=PostPostLink.post_to_id==id,
		backref=backref("back_connectionItems")
    )'''
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('posts', uselist=True))
    def getconnections(self):
        return self.connections+self.back_connections
    def printout(self):
        print "\nPOST:"+self.name
        print "-by: "+ self.author.name
        print "-connections"
        for c in self.getconnections():
            print "--",c.name
        for ci in self.back_connectionItems:
            print ci.post_from.name, ci.type, ci.post_to.name
	    print "votenum: ", self.votenum, "  rating: ", self.rating
        print "----------\n"
class VotePost(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    created = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('votes', uselist=True))
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship(Post, backref=backref('votes', uselist=True))
