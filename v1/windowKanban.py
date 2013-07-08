#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import wx
import DragCanvas
import Kanban
import pickle
import zipfile
from parserimg import Parser
from wx.lib.wordwrap import wordwrap # contenedores que albergan texto
import wx.lib.agw.cubecolourdialog as CCD # para cambiar color de fondo
import cv2
import numpy as np 
from Postit import *

class windowKanban():
    # recibe un objeto Kanban que contiene el kanban
    def __init__(self, kanban, pos=(50,50)):
        self.app = wx.PySimpleApp()
        self.pos = pos
    
    #self.frame = wx.Frame(None, wx.NewId(), "hola", pos, size=(kanban.sizeX, kanban.sizeY), style=wx.DEFAULT_FRAME_STYLE)
    #self.frame.Show(1)

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
        m_new = menu.Append(wx.NewId(), "&Importar imagen", "Crea un nuevo tablero a partir de una imagen.")
        m_newWindow = menu.Append(wx.NewId(), "&Nueva ventana", "Crea una ventana Skabnan.")
        m_save = menu.Append(wx.NewId(), "&Guardar", "Guarda los cambios en fichero skb.")
        m_load = menu.Append(wx.NewId(), "&Cargar", "Carga un tablero a partir de un archivo *.skb")

        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onNew, m_new)
        self.frame.Bind(wx.EVT_MENU, self.onNewWindow, m_newWindow)
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
        #m_addVerticalLine = menu.Append(wx.NewId(), "Agregar linea &Horizontal", "Agrega una linea vertical en la posicion donde se hace clic")
        #m_addHorizontalLine = menu.Append(wx.NewId(), "Agregar linea &Vertical", "Agrega una linea horizontal en la posicion donde se hace clic")

        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onAddPostIt, m_addPostIt)
        self.frame.Bind(wx.EVT_MENU, self.onChangeColor, m_changeColor)
        #self.frame.Bind(wx.EVT_MENU, self.onAddVerticalLine, m_addVerticalLine)
        #self.frame.Bind(wx.EVT_MENU, self.onAddHorizontalLine, m_addHorizontalLine)
        
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
        self.frame.dc = DragCanvas.DragCanvas(self.frame, kanban)

        #guardo el kanban para despues cortar la imagen
        self.kanban = kanban

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

        self.kanban = kanban
        self.frame.dc.reInit(kanban)

    def onNewWindow(self, event):

        parser = Parser()
        kanban = parser.parse("Skanban.jpg")
        sk = windowKanban(kanban, (self.pos[0]+50, self.pos[1]+50))
        sk.showKanban()

    def onSave(self, event):
        print "save"
        fd = wx.FileDialog(self.frame, "Selecione un directorio", style=wx.FD_SAVE)

        if fd.ShowModal() == wx.ID_CANCEL:
            return

        self.kanban.save(fd.GetPath()+".skb")
    
    def onLoad(self, event):
        print "load"
        fd = wx.FileDialog(self.frame, "Selecione un archivo *.skb")
        fd.SetWildcard("Archivo (*.skb)|*.skb")

        if fd.ShowModal() == wx.ID_CANCEL:
            return

        dirname = ""
        z = zipfile.ZipFile(fd.GetPath())
        for f in z.namelist():
            (dirname, filename) = os.path.split(f)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            
            outfile = open(f, 'wb')
            outfile.write(z.read(f))
            outfile.close()
        z.close()

        # lee pkl y se crea una ventana con los objetos
        print "DIRIDIRIDIR"+os.path.join(dirname, "data.pkl")
        self.kanban = pickle.load(open(os.path.join(dirname, "data.pkl"), "rb"))

        self.frame.dc.reInit(self.kanban)
        #sk = windowKanban(kanban, (self.pos[0]+50, self.pos[1]+50))
        #sk.showKanban()

    def onAddPostIt(self, event):
        dlg = AddPostitPanel(self.kanban, self.frame, -1, "Agregar postit manualmente", size=(350, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()

        #self.frame = wx.Frame(None, title='Photo Control')
        #self.frame.Show(True)
        
    def onChangeColor(self, event):
        if not hasattr(self, "colourData"):
            self.colourData = wx.ColourData()
        
        self.colourData.SetColour(self.frame.dc.GetBackgroundColour())
        
        dlg = CCD.CubeColourDialog(self.frame.dc, self.colourData)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            self.colourData = dlg.GetColourData()
            
            self.frame.dc.SetBackgroundColour(self.colourData.GetColour())
            self.frame.dc.Refresh()
            self.frame.kanban.background = self.colourData.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            self.frame.kanban.save()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()

    def onAddVerticalLine(self, event):
        pass

    def onAddHorizontalLine(self, event):
        pass

    def onAbout(self, event):
        # se crea y completa un objeto info
        info = wx.AboutDialogInfo()
        info.Name = "Skanban"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2013 "
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

        licenseText = "Copyright (C) 2013  Equipo Skanban\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>."

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

class AddPostitPanel(wx.Dialog):
    def __init__(
            self, kanban, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            ):
        self.parent = parent
        self.nPoints = []
        self.kanban = kanban
        self.img = cv2.imread(kanban.resized_path)
        
        size = (self.img.shape[1], self.img.shape[0])

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)


        # Now continue with the normal construction of the dialog
        # contents
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        

        #sizer = wx.BoxSizer(wx.VERTICAL)
        #self.SetSizeHints(minW=)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)


    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap(self.kanban.resized_path)
        dc.DrawBitmap(bmp, 0, 0)


    def OnMouse(self, event):
        if event.LeftDown():
            dc = wx.ClientDC(self)
            dc.SetBrush(wx.Brush('#ff0000'))
            dc.DrawCircle(event.GetX(), event.GetY(), 3)
            self.nPoints+=[[[event.GetX(), event.GetY()]]]
            if len(self.nPoints)>=4:
                self.cutPostit()

    def cutPostit(self):
        print "cuting"
        rect = cv2.boundingRect(np.array(self.nPoints))
        x,y,w,h = rect
        img = self.img

        postits = [np.array(self.nPoints)]

        parser = Parser()
        img = parser.removeBackground(img,x,y,w,h,postits[0])
        path_ = parser.saveImage(self.kanban.path, len(self.kanban.postits)+1, img)
        self.kanban.postits.append(Postit(path_, x, y, w, h))
        self.kanban.save()
        
        self.parent.dc.reInit(self.kanban)
        self.Destroy()
