__author__ = 'chozabu'

import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased


Base = declarative_base()



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

class GroupMembershipLink(Base):
    __tablename__ = 'group_membership_link'
    #id = Column(Integer, primary_key=True)
    type = Column(String)
    author_id = Column(ForeignKey('author.id'), primary_key=True)
    group_id = Column(ForeignKey('group.id'), primary_key=True)
    author = relationship(
        'Author',
		primaryjoin='GroupMembershipLink.author_id==Author.id',
		backref=backref("group_memberships")
    )
    group = relationship(
        'Group',
		primaryjoin='GroupMembershipLink.group_id==Group.id',
		backref=backref("memberships")
    )

class CatagoryMembershipLink(Base):
    __tablename__ = 'catagory_membership_link'
    #id = Column(Integer, primary_key=True)
    type = Column(String)
    author_id = Column(ForeignKey('author.id'), primary_key=True)
    catagory_id = Column(ForeignKey('catagory.id'), primary_key=True)
    author = relationship(
        'Author',
		primaryjoin='CatagoryMembershipLink.author_id==Author.id',
		backref=backref("catagory_memberships")
    )
    catagory = relationship(
        'Catagory',
		primaryjoin='CatagoryMembershipLink.catagory_id==Catagory.id',
		backref=backref("memberships")
    )
class AuthorAuthorRepLink(Base):
    __tablename__ = 'author_author_rep_link'
    #id = Column(Integer, primary_key=True)
    type = Column(String)
    catagory_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship('Catagory', backref=backref('reps', uselist=True))
    author_from_id = Column(ForeignKey('author.id'), primary_key=True)
    author_to_id = Column(ForeignKey('author.id'), primary_key=True)
    author_from = relationship(
        'Author',
		primaryjoin='AuthorAuthorRepLink.author_from_id==Author.id',
		backref=backref("representers")
    )
    author_to = relationship(
        'Author',
		primaryjoin='AuthorAuthorRepLink.author_to_id==Author.id',
		backref=backref("representees")
    )
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer)
    rating = Column(Float)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('comments', uselist=True))
    created = Column(DateTime, default=func.now())
    text = Column(String)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", backref=backref('comments', uselist=True))
    parent_id = Column(Integer, ForeignKey('comment.id'))
    children = relationship("Comment",
                backref=backref('parent', remote_side=[id])
                )
class Catagory(Base):
    __tablename__ = 'catagory'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer)
    rating = Column(Float)

    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('catagorys_created', uselist=True))

    created = Column(DateTime, default=func.now())
    name = Column(String)

    #posts = relationship("Post", backref="catagory")
    
    
    parent_id = Column(Integer, ForeignKey('catagory.id'))
    children = relationship("Catagory",
                backref=backref('parent', remote_side=[id])
                )
class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer)
    rating = Column(Float)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('tags', uselist=True))
    created = Column(DateTime, default=func.now())
    text = Column(String)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship("Post", backref=backref('tags', uselist=True))

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer, default=0)
    rating = Column(Float, default=0)
    catagory_id = Column(Integer, ForeignKey('catagory.id'))
    catagory = relationship(Catagory, backref=backref('posts', uselist=True))
    created = Column(DateTime, default=func.now())
    name = Column(String)
    connections = relationship(
        'Post',
        secondary="post_post_link",
		primaryjoin=PostPostLink.post_from_id==id,
		secondaryjoin=PostPostLink.post_to_id==id,
		backref=backref("back_connections")
    )
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
class VoteComment(Base):
    __tablename__ = 'commentvote'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    created = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('commentvotes', uselist=True))
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment = relationship(Comment, backref=backref('votes', uselist=True))
class VoteTag(Base):
    __tablename__ = 'tagvote'
    id = Column(Integer, primary_key=True)
    value = Column(Float)
    created = Column(DateTime, default=func.now())
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('tagvotes', uselist=True))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    tag = relationship(Tag, backref=backref('votes', uselist=True))


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    votenum = Column(Integer)
    rating = Column(Float)

    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author, backref=backref('groups_created', uselist=True))

    created = Column(DateTime, default=func.now())
    name = Column(String)

    #posts = relationship("Post", backref="group")
    
    
    parent_id = Column(Integer, ForeignKey('group.id'))
    children = relationship("Group",
                backref=backref('parent', remote_side=[id])
                )