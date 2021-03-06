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
from  wx.lib.intctrl import *
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
        m_save = menu.Append(wx.NewId(), "&Guardar como...", "Guarda los cambios en fichero skb.")
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
        m_addText = menu.Append(wx.NewId(), "&Agregar Texto", "Agregar texto manualmente al kanban")
        m_changeColor = menu.Append(wx.NewId(), "&Cambiar color fondo", "Cambia el color de fondo de la ventana")
        m_drawLine = menu.Append(wx.NewId(), "&Dibujar Linea", "Dibuja una linea en base a dos coordenadas")
        m_showOriginal = menu.Append(wx.NewId(), "&Mostrar imagen original", "Muestra la imagen original en gris", wx.ITEM_CHECK)
        #m_addVerticalLine = menu.Append(wx.NewId(), "Agregar linea &Horizontal", "Agrega una linea vertical en la posicion donde se hace clic")
        #m_addHorizontalLine = menu.Append(wx.NewId(), "Agregar linea &Vertical", "Agrega una linea horizontal en la posicion donde se hace clic")

        # se asocia un metodo al evento clic del elemento del menu
        self.frame.Bind(wx.EVT_MENU, self.onAddPostIt, m_addPostIt)
        self.frame.Bind(wx.EVT_MENU, self.onAddText, m_addText)
        self.frame.Bind(wx.EVT_MENU, self.onChangeColor, m_changeColor)
        self.frame.Bind(wx.EVT_MENU, self.onDrawLine, m_drawLine)
        self.frame.Bind(wx.EVT_MENU, self.onShowOriginal, m_showOriginal)
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
        print "new"

        fd = wx.FileDialog(self.frame, "Selecione una imagen")
        fd.SetWildcard("Imagenes (*.bmp, *.jpg, *.jpeg, *.png)|*.jpg;*.bmp;*.jpeg;*.png")
        
        if fd.ShowModal() == wx.ID_CANCEL:
            return

        dlg = MinMaxDialog(self.frame, -1, "Tamaño Post-its", size=(350, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                         )

        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()

        min_postit = int(dlg.min.GetValue())
        max_postit = int(dlg.max.GetValue())


        dlg.Destroy()

        if val != wx.ID_OK:
            return


        parser = Parser()
        kanban = parser.parse(fd.GetPath(), min_postit, max_postit)

        self.kanban = kanban
        self.frame.dc.reInit(kanban)
        self.frame.SetSizeWH(self.kanban.sizeX,self.kanban.sizeY)
        self.frame.kanban = kanban

    def onNewWindow(self, event):
        print "newWindow"

        parser = Parser()
        kanban = parser.parse("Skanban.jpg")
        sk = windowKanban(kanban, (self.pos[0]+50, self.pos[1]+50))
        sk.showKanban()

    def onSave(self, event):
        #print "save"
        fd = wx.FileDialog(self.frame, "Selecione un directorio", style=wx.FD_SAVE)

        if fd.ShowModal() == wx.ID_CANCEL:
            return
	path = fd.GetPath()

	if path[-4:]!='.skb':
		path = path+'.skb'
        self.kanban.save(path)
    
    def onLoad(self, event):
        #print "load"
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
        self.kanban = pickle.load(open(os.path.join(dirname, "data.pkl"), "rb"))

        self.frame.kanban = self.kanban

        self.frame.dc.reInit(self.kanban)
        #print "background", self.kanban.background
        self.frame.dc.SetBackgroundColour(self.kanban.background)
        self.frame.dc.Refresh()

        self.frame.SetSizeWH(self.kanban.sizeX,self.kanban.sizeY)
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
        
        ############
        
    def onAddText(self, event):
        
        dlg = wx.TextEntryDialog(
        self.frame, 'Ingrese el texto a insertar','Ingreso de texto', 'Python')

        dlg.SetValue("Skanban!")
        if dlg.ShowModal() == wx.ID_OK and len(dlg.GetValue()) > 50:
            dlg = wx.MessageDialog(self.frame, 'Texto demasiado largo',
                               'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()  
            return   
        elif len(dlg.GetValue())!=0:
            text = dlg.GetValue()
      
        else:
            return
        dlg.Destroy()
        
        #bg_colour = wx.Colour(57, 115, 57)  # matches the bg image
        font = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD)
        textExtent = self.frame.dc.GetFullTextExtent(text, font)
        
        # create a bitmap the same size as our text
        #np_array = np.array(textExtent[0], textExtent[1])

        np_array = np.zeros((textExtent[1], textExtent[0] + 2, 1), np.uint8)
        
        #np_array = cv2.cvtColor(np_array, cv2.COLOR_BGR2GRAY)
        
        # 'draw' the text onto the bitmap
        #self.frame.dc.SelectObject(bmp)
        #self.frame.dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        #self.frame.dc.Clear()
        """
        self.frame.dc.SetTextForeground(wx.RED)
        self.frame.dc.SetFont(font)
        self.frame.dc.DrawText(text, 0, 0)
        self.frame.dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(bmp, bg_colour)
        bmp.SetMask(mask)
        shape = DragShape(bmp)
        shape.pos = (5, 100)
        shape.text = "Some dragging text"
        self.shapes.append(shape)
        """
        # ancho y alto
        h = textExtent[1]
        w = textExtent[0]
        
       	#img = cv2.putText(np_array, text , (12,12), cv2.FONT_HERSHEY_PLAIN, 1,  255)
       	cv2.putText(np_array, text, (5, h-5), cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(255,255,255), thickness=1)
        
        # posicion por defecto donde aparece el texto
        x = 20
        y = 20
        
        # para guardar una imagen del texto y tratarlo como un postit
        parser = Parser()
        path_ = parser.saveImage(self.kanban.path, len(self.kanban.postits)+1, np_array)
        self.kanban.postits.append(Postit(path_, x, y, w, h))
        self.kanban.save()        
        
        self.frame.dc.reInit(self.kanban)
        
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

    def onDrawLine(self, event):
        self.frame.dc.DrawLine()

    def onAddVerticalLine(self, event):
        pass

    def onAddHorizontalLine(self, event):
        pass

    def onShowOriginal(self, event):
        if event.Checked():
            print "checked"
            self.frame.dc.isBackgroundActive = True
            bg_bitmap = wx.Bitmap(self.kanban.resized_path)
            bg_image = bg_bitmap.ConvertToImage()
            bg_image = bg_image.ConvertToGreyscale()
            bg_bitmap = bg_image.ConvertToBitmap()
            self.frame.dc.bg_bmp = bg_bitmap
            self.frame.dc.Refresh()
        else:
            print "unchecked"
            self.frame.dc.isBackgroundActive = False
            self.frame.dc.bg_bmp = None
            self.frame.dc.Refresh()

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

class MinMaxDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

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
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Ingrese tamaño mínimo y máximo de los elementos")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tamaño Mínimo:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = IntCtrl(self, -1, 1000, size=(80,-1))
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.min = text
        #self.min.Bind(wx.EVT_CHAR, self.handle_number)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tamaño Máximo:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        text = IntCtrl(self, -1, 50000, size=(80,-1))
        box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.max = text
        #self.max.Bind(wx.EVT_CHAR, self.handle_number)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        self.btn_ok = btn

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        self.btn_cancel = btn

        self.Bind(EVT_INT, self.SetTargetMinMax, self.min)
        self.Bind(EVT_INT, self.SetTargetMinMax, self.max)

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def handle_number(self, event):
        keycode = event.GetKeyCode()

        if keycode < 255:
            if chr(keycode).isdigit():
                event.Skip()

    def SetTargetMinMax( self, event=None ):
        min = max = None

        if self.min.GetValue():
            min = self.min.GetValue()

        if self.max.GetValue():
            max = self.max.GetValue()

        if min >= max:
            self.max.SetForegroundColour( wx.RED )
            self.min.SetForegroundColour( wx.RED )
            self.btn_ok.Disable()
        else:
            self.max.SetForegroundColour( wx.BLACK )
            self.min.SetForegroundColour( wx.BLACK )
            self.btn_ok.Enable()


        self.max.Refresh()
        self.min.Refresh()


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
        #print "cuting"

        #ver si no se cruzan las lineas
        
        if self.intersect(self.nPoints[0][0],self.nPoints[1][0],self.nPoints[2][0],self.nPoints[3][0]):
            
            aux = self.nPoints[1][0]
            self.nPoints[1][0] = self.nPoints[2][0]
            self.nPoints[2][0] = aux 
        elif self.intersect(self.nPoints[1][0],self.nPoints[2][0],self.nPoints[3][0],self.nPoints[0][0]):
            aux = self.nPoints[2][0]
            self.nPoints[2][0] = self.nPoints[3][0]
            self.nPoints[3][0] = aux 
            
        rect = cv2.boundingRect(np.array(self.nPoints))
        x,y,w,h = rect
        img = self.img

        postits = [np.array(self.nPoints)]

        parser = Parser()
        img = parser.removeBackground(img,x,y,w,h,postits[0])
        path_ = parser.saveImage(self.kanban.path, self.kanban.serial, img)
        #print "CUT 1 tengo",len(self.kanban.postits)
        self.kanban.addPostit(Postit(path_, x, y, w, h))
        #self.kanban.postits.append(Postit(path_, x, y, w, h))
        self.kanban.save()
        #print "CUT 2 tengo",len(self.kanban.postits)
        
        self.parent.dc.reInit(self.kanban)
        self.Destroy()

    def intersect(self, p1, p2, p3, p4):

        if p1[0]-p2[0] != 0:
            m12 = 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])
        else:
            m12 = 'inf'

        if p3[0]-p4[0] != 0:
            m34 = 1.0*(p3[1]-p4[1])/(p3[0]-p4[0])
        else:
            m34 = 'inf'

        if m12 == m34:
            return False

        if m12 == 'inf':
            y = m34*(p1[0]-p3[0]) + p3[1]
            if p1[0]>=min(p3[0], p4[0]) and p1[0]<= max(p3[0], p4[0]) and y>=min(p1[0], p2[0]) and y<=max(p1[0],p2[0]):
                return True
            return False
        
        if m34 == 'inf':
            y = m12*(p3[0]-p1[0]) + p1[1]
            if p3[0]>=min(p1[0], p2[0]) and p3[0]<= max(p1[0], p2[0]) and y>=min(p3[0], p4[0]) and y<=max(p3[0],p4[0]):
                return True
            return False

        
        x = (m12*p1[0]-m34*p3[0]+p3[1]-p1[1])/(m12-m34)
        y = m12*(x-p1[0]) + p1[1]
        
        if x>= min(p1[0],p2[0]) and x<=max(p2[0],p1[0]) and y>= min(p3[1],p4[1]) and y<=max(p3[1],p4[1]):
            return True

        return False
