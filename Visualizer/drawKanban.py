import sys
import wx
import DragCanvas
sys.path.insert(0,"../loader/")
import Board

class drawKanban():
    # recibe un objeto Board que contiene el kanban
    def __init__(self, kanban):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame(None, -1, kanban.title, pos=(50,50), size=(kanban.sizeX, kanban.sizeY), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")

        # recibe la imagen de fondo y una lista de los objetos postIt
        self.dc = DragCanvas.DragCanvas(self.frame,-1, kanban.background, kanban)

    def showKanban(self):
        self.frame.Show(1)
        self.app.MainLoop()
