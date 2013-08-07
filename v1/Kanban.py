#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

from Postit import Postit
"""
import pickle
import os, zipfile

class Kanban(object):
    # __tablename__ = 'board'
    # id = Column(Integer, primary_key=True)
    # postits = []
    # title = Column(String)
    # background = Column(String)
    # sizeX = Column(Integer)
    # sizeY = Column(Integer)

    id = 0
    postits = []
    title = ""
    background = ""
    sizeX = 0
    sizeY = 0
    path = ""
    resized_path = ""
    skb_file = ""
    serial = 0

    def __init__(self, postits=[], title = "", background="", sizeX=800, sizeY=600):
        self.postits = postits
        self.title = title
        self.background = background
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.lines = []
    
    def addPostit(self, p):
        self.postits.append(p)
        self.serial+=1

    def getPKLPath(self):
        return os.path.join('images',self.title,'data.pkl')

    def save(self, skb_file_=""):
        if skb_file_:
            self.skb_file = skb_file_

        fp = open(self.getPKLPath(), 'w+')
        pickle.dump(self, fp)
        fp.close()

        if self.skb_file:
            self.saveToSKB()
        
    def saveToSKB(self):
        mizipfile = zipfile.ZipFile(self.skb_file, mode = "w")
        
        head, tail = os.path.split(self.postits[0].path)
        head2, tail2 = os.path.split(head)

        #print os.path.join("images", tail2)
        #print self.kanban.title + ".pkl"

        for postit in self.postits:
            mizipfile.write(postit.path)
        
        print self.getPKLPath()
        mizipfile.write(self.getPKLPath())
        mizipfile.write(self.resized_path)

        mizipfile.close()

    @staticmethod
    def load(title):
        fp = open(self.getPKLPath(), 'r')
        return pickle.load(fp)

    # def persist(self):
        # con = None

        # try:
            # con = lite.connect('skanban.db')
            
            # cur = con.cursor()    
            # cur.execute('SELECT * FROM board WHERE board.')
            
            # data = cur.fetchone()
            
            # print "SQLite version: %s" % data                
            
        # except lite.Error, e:
            
            # print "Error %s:" % e.args[0]
            # sys.exit(1)
            
        # finally:
            
            # if con:
                # con.close()
