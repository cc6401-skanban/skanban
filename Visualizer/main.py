import sys
import wx
from drawKanban import drawKanban
sys.path.insert(0,"../parser/")
sys.path.insert(0,"../loader/")
from parserimg import Parser
from Board import Board

def main():

    # se inicializa la base de datos
	
	# se carga un kanban
    parser = Parser()
    kanban = parser.parse("../image.jpg")
    for postit in kanban.postits:
		print postit.path
	# se crea una ventana kanban
    sk = drawKanban(kanban)
	
	# mostrar kanban
    sk.showKanban()

if __name__ == "__main__":
    main()