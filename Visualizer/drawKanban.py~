import sys 
sys.path.insert(0,"../loader/")
import Board

class drawKanban():
	# recibe un objeto Board que contiene el kanban
    def __init__(self, kanban):
        app = wx.PySimpleApp()
        frame = wx.Frame(None, -1, kanban.title, pos=(50,50), size=(kanban.sizeX, kanban.sizeY), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
	
	# recibe la imagen y una lista de los objetos postIt
    dc = DragCanvas.DragCanvas(frame,-1, kanban.background, kanban.postits)
	
	def showKanban():
        frame.Show(1)
	    app.MainLoop()
