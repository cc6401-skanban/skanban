import sys
import wx
import DragCanvas
import Board
from parserimg import Parser
from wx.lib.wordwrap import wordwrap # contenedores que albergan texto
import wx.lib.agw.cubecolourdialog as CCD # para cambiar color de fondo

class windowKanban():
    # recibe un objeto Board que contiene el kanban
    def __init__(self, kanban, pos=(50,50)):
        self.app = wx.PySimpleApp()
        self.pos = pos

        # se crea la ventana
        self.frame = wx.Frame(None, 
            wx.NewId(), 
            kanban.title, 
            pos, 
            size=(kanban.sizeX, kanban.sizeY), 
            style=wx.DEFAULT_FRAME_STYLE, 
            name="Skanban")

        #####################################################################################
        # Creacion del menu de la ventana principal                                         #
        #####################################################################################
        # crea un menu de barra (aparece en la parte superior de la ventana) 
        menuBar = wx.MenuBar()

        # menu Archivo
        #####################################################################################
        menu = wx.Menu()
        
        # elementos de la lista del menu Archivo
        m_new = menu.Append(wx.NewId(), "&Nuevo", "Crea un nuevo tablero a partir de una imagen.")
        m_save = menu.Append(wx.NewId(), "&Guardar", "Guarda las posiciones de un tablero.")
        m_load = menu.Append(wx.NewId(), "&Cargar", "Carga un tablero a partir de un archivo *.pkl.")

        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onNew, m_new)
        self.frame.Bind(wx.EVT_MENU, self.onSave, m_save)
        self.frame.Bind(wx.EVT_MENU, self.onLoad, m_load)

        # se agrega el menu 'Archivo' al menuBar
        menuBar.Append(menu, "&Archivo")

        # menu Editar
        #####################################################################################
        menu = wx.Menu()

        # elementos de la lista del menu Editar
        m_addPostIt = menu.Append(wx.NewId(), "&Agregar post-it", "Agregar post-it manualmente al kanban")
        m_changeColor = menu.Append(wx.NewId(), "&Cambiar color fondo", "Cambia el color de fondo de la ventana")
        
        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onAddPostIt, m_addPostIt)
        self.frame.Bind(wx.EVT_MENU, self.onChangeColor, m_changeColor)
        
        # se agrega el menu 'Editar' al menuBar
        menuBar.Append(menu, "&Editar")

        # menu ? 
        #####################################################################################
        menu = wx.Menu()

        # elementos de la lista del menu ?
        m_about = menu.Append(wx.NewId(), "&Acerca de ...", "Informacion de sus creadores.")

        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onAbout, m_about)
        
        # se agrega el menu '?' al menuBar
        menuBar.Append(menu, "&?")

        self.frame.SetMenuBar(menuBar)

        # recibe el marco y un kanban para dibujar
        self.dc = DragCanvas.DragCanvas(self.frame, kanban)

    def showKanban(self):
        self.frame.Show(1)
        self.app.MainLoop()

    #####################################################################################
    # Eventos del menu                                                                  #
    #####################################################################################
    def onNew(self, event):
        fd = wx.FileDialog(self.frame, "Selecione una imagen")
        fd.SetWildcard("Imagenes (*.bmp, *.jpg, *.jpeg, *.png)|*.jpg;*.bmp;*.jpeg;*.png")
        
        if fd.ShowModal() == wx.ID_CANCEL:
            return

        parser = Parser()
        kanban = parser.parse(fd.GetPath())

        sk = windowKanban(kanban, (self.pos[0]+50, self.pos[1]+50))
        sk.showKanban()

    def onSave(self, event):
        print "save"

    def onLoad(self, event):
        print "load"
        fd = wx.FileDialog(self.frame, "Selecione un archivo *.pkl")
        fd.SetWildcard("Archivo (*.pkl)|*.pkl")

        if fd.ShowModal() == wx.ID_CANCEL:
            return

        # lee pkl y se crea una ventana con los objetos

        sk = windowKanban(kanban, (self.pos[0]+50, self.pos[1]+50))
        sk.showKanban()
        
    def onAddPostIt(self, event):
        print "addPostIt"
        
    def onChangeColor(self, event):
        if not hasattr(self, "colourData"):
            self.colourData = wx.ColourData()
        
        self.colourData.SetColour(self.dc.GetBackgroundColour())
        
        dlg = CCD.CubeColourDialog(self.dc, self.colourData)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            self.colourData = dlg.GetColourData()
            
            self.dc.SetBackgroundColour(self.colourData.GetColour())
            self.dc.Refresh()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()

    def onAbout(self, event):
        # se crea y completa un objeto info
        info = wx.AboutDialogInfo()
        info.Name = "Skanban"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2013 blah blah blah"
        info.Description = wordwrap(
            "Este programa ha sido disenado para el curso " 
            "CC6401-1 Taller de Metodologias Agiles de Desarrollo de Software "

            "\n\n Utilizalo con sabiduria.",
            350, wx.ClientDC(self.frame))
        info.WebSite = ("https://github.com/cc6401-skanban/skanban", "Repositorio GitHub")
        info.Developers = [ "Javiera A. Born B.",
                            "Eduardo E. A. Frias M.",
                            "Francisco Y. Hafon A.",
                            "Felipe A. Hernandez G.",
                            "Nicolas M. Miranda C.",
                            "Ivan Pliouchtchai",
                            "Matias Toro I."]

        licenseText = "Esta es la licencia"

        info.License = wordwrap(licenseText, 500, wx.ClientDC(self.frame))

        # Se llama a wx.AboutBox dandole el objeto info
        wx.AboutBox(info)

    #def OnClose(self, event):
    #    dlg = wx.MessageDialog(self,
     #   "Do you really want to close this application?",
      #  "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
    #    result = dlg.ShowModal()
    #    dlg.Destroy()
   #     if result == wx.ID_OK:
   #         self.Destroy()
  
    #def OnAbout(self, event):
    #    dlg = AboutBox()
   #     dlg.ShowModal()
   #     dlg.Destroy()