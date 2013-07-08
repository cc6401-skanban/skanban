#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import wx
from windowKanban import windowKanban
from parserimg import Parser
from Kanban import Kanban

def main():

	# se carga un kanban
    parser = Parser()
    if( len(sys.argv) < 2):
        kanban = parser.parse("Skanban.jpg")
    else:
        kanban = parser.parse(sys.argv[1])
	
    # se crea una ventana kanban
    wk = windowKanban(kanban)
	
	# mostrar kanban
    wk.showKanban()
    
if __name__ == "__main__":
    main()
