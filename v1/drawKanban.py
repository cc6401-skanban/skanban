import sys
import wx
import DragCanvas
import Board
import button

class drawKanban():
    # recibe un objeto Board que contiene el kanban
    def __init__(self, kanban, pos=(50,50)):
        self.app = wx.PySimpleApp()
        self.pos = pos
        #self.frame = wx.Frame(None, -1, kanban.title, pos=(50,50), size=(kanban.sizeX, kanban.sizeY), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        self.frame = wx.Frame(None, -1, "asdfasdf", pos, size=(800, 600), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        
        # se crea un menu de barra (aparece en la parte superior) 
        menuBar = wx.MenuBar()
        # menu Archivo
        menu = wx.Menu()
        # elemento de la lista del menu Archivo
        m_new = menu.Append(wx.NewId(), "&Nuevo\tAlt-n", "Crea un nuevo tablero a partir de una imagen.")
        m_save = menu.Append(wx.NewId(), "&Guardar\tAlt-s", "Guarda las posiciones de un tablero.")
        m_load = menu.Append(wx.NewId(), "&Cargar\tAlt-l", "Carga un tablero a partir de un archivo *.pkl.")

        # se asocia un un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onNew, m_new)
        self.frame.Bind(wx.EVT_MENU, self.onSave, m_save)
        self.frame.Bind(wx.EVT_MENU, self.onLoad, m_load)

        # se agrega el menu al menuBar
        menuBar.Append(menu, "&Archivo")

        # menu Editar
        menu = wx.Menu()

        m_addPostIt = menu.Append(wx.NewId(), "&Agregar post-it", "Agregar post-it manualmente al kanban")
        self.frame.Bind(wx.EVT_MENU, self.onAddPostIt, m_addPostIt)
        
        menuBar.Append(menu, "&Editar")

        self.frame.SetMenuBar(menuBar)

        # recibe la imagen de fondo y una lista de los objetos postIt
        #self.dc = DragCanvas.DragCanvas(self.frame,-1, kanban.background, kanban)

    def showKanban(self):
        self.frame.Show(1)
        self.app.MainLoop()

    def onNew(self, event):
        print "new"
        fd = wx.FileDialog(self.frame, "Selecione una imagen")
        fd.SetWildcard("Imagenes (*.bmp, *.jpg, *.jpeg, *.png)|*.jpg;*.bmp;*.jpeg;*.png")
        fd.ShowModal()
        file_path = fd.GetPath()

        sk = drawKanban(None, (self.pos[0]+50, self.pos[1]+50))
        sk.showKanban()

    def onSave(self, event):
        print "save"

    def onLoad(self, event):
        print "load"

    def onAddPostIt(self, event):
        print "addPostIt"


    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
        "Do you really want to close this application?",
        "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
  
    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()