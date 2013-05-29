from sqlalchemy import *
from Postit import Postit
from Board import Board

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class persister:

    engine = create_engine('postgresql:///root:storm@localhost/skanban', echo=True)
    Base.metadata.create_all(engine) 
    
    """
	metadata = MetaData()
	
	## Crear tablas si aun no existen
	postit_table = Table('postit', metadata,
	Column('id', Integer, primary_key=True),
	Column('path', String(512)),
	Column('posX', Integer),
	Column('posY', Integer),
	Column('sizeX', Integer),
	Column('sizeY', Integer)
	)
	
	#Falta! agregar el arreglo postits a la bd... hay que hacer otra tabla, supongo
	#postits = []

	board_table  = Table('board', metadata,
	Column('id', Integer, primary_key=True),
	Column('title', String(200)),
	Column('background', String(200)),
	Column('sizeX', Integer),
	Column('sizeY', Integer)
	)
	
	metadata.create_all(engine) 

	##Asociar las tablas a las clases
	mapper(Postit, postit_table) 
	mapper(Board, board_table)
	


	def createPostit(self, path="", posX=0, posY=0, sizeX=0, sizeY=0):
		i = self.postitBD.insert()
		i.execute({'path':path, 'posX':posX, 'posY':posY,  'sizeX':sizeX, 'sizeY':sizeY})
		result.last_inserted_ids()
		#retornar el postit creado

	def loadPostit(self,id):
		pass
    """

persister()
