import sys
import wx
from drawKanban import drawKanban
from parserimg import Parser
from Board import Board

def main():

    # se inicializa la base de datos
	
	# se carga un kanban
    parser = Parser()
    #kanban = parser.parse("../image4.jpg")
    #for postit in kanban.postits:
	#	print postit.path
	## se crea una ventana kanban
    sk = drawKanban(None)#kanban)
	#
	# mostrar kanban
    sk.showKanban()
if __name__ == "__main__":
    main()
