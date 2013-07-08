import sys
import wx
from windowKanban import windowKanban
from parserimg import Parser
from Board import Board

def main():

	# se carga un kanban
    parser = Parser()
    if( len(sys.argv) < 2):
        kanban = parser.parse("Skanban.jpg")
    else:
        kanban = parser.parse(sys.argv[1])
    #for postit in kanban.postits:
    #	print postit.path
	
    # se crea una ventana kanban
    wk = windowKanban(kanban)
	
	# mostrar kanban
    wk.showKanban()
if __name__ == "__main__":
    main()
