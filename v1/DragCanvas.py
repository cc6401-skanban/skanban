#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
from dragShape import DragShape
from Line import Line

#----------------------------------------------------------------------

class DragCanvas(wx.ScrolledWindow):
    def __init__(self, parent, board):
        wx.ScrolledWindow.__init__(self, parent, wx.NewId())

        self.board = board
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None
        self.isDrawingLine = False
        self.isBackgroundActive = False
        self.lineCoordinates = []

        self.parent = parent

        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        #self.bg_bmp = wx.Image(opj("Fondo.jpg"), wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        
        # se carga cada post-it en un arreglo de shape
        arrPostIts = board.postits
        for x in range(len(arrPostIts)):
            bmp = wx.Image(opj(arrPostIts[x].path), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        

        # bmp = wx.Image(opj('horse.png'), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        # shape = DragShape(bmp)
        # shape.pos = (200, 5)
        # self.shapes.append(shape)

        # Make a shape from some text
        # text = "Some Text"
        # bg_colour = wx.Colour(57, 115, 57)  # matches the bg image
        # font = wx.Font(15, wx.ROMAN, wx.NORMAL, wx.BOLD)
        # textExtent = self.GetFullTextExtent(text, font)

        #create a bitmap the same size as our text
        # bmp = wx.EmptyBitmap(textExtent[0], textExtent[1])

        #'draw' the text onto the bitmap
        # dc = wx.MemoryDC()
        # dc.SelectObject(bmp)
        # dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        # dc.Clear()
        # dc.SetTextForeground(wx.RED)
        # dc.SetFont(font)
        # dc.DrawText(text, 0, 0)
        # dc.SelectObject(wx.NullBitmap)
        # mask = wx.Mask(bmp, bg_colour)
        # bmp.SetMask(mask)
        # shape = DragShape(bmp)
        # shape.pos = (5, 100)
        # shape.text = "Some dragging text"
        # self.shapes.append(shape)

        # se asocian los metodos a cada evento
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.reInit(board)

    def reInit(self, board): 
        self.board = board
        arrPostIts = board.postits
        self.shapes = []
        self.dragImage = None
        self.dragShape = None
        self.delShape = None
        self.hiliteShape = None

        for x in range(len(arrPostIts)):
            bmp = wx.Image(opj(arrPostIts[x].path), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
            shape = DragShape(bmp)
            shape.pos = arrPostIts[x].getPosition()
            shape.postit = arrPostIts[x]
            shape.fullscreen = True
            self.shapes.append(shape)

        for line in self.board.lines:
            self.shapes.append(line)

        self.Refresh()
    
    # We're not doing anything here, but you might have reason to.
    # for example, if you were dragging something, you might elect to
    # 'drop it' when the cursor left the window.
    def OnLeaveWindow(self, evt):
        pass

    # tile the background bitmap
    def TileBackground(self, dc):

        if self.isBackgroundActive:
            sz = self.GetClientSize()
            w = self.bg_bmp.GetWidth()
            h = self.bg_bmp.GetHeight()
            x = 0
        
            while x < sz.width:
                y = 0
        
                while y < sz.height:
                    dc.DrawBitmap(self.bg_bmp, x, y)
                    y = y + h
        
                x = x + w


    # Go through our list of shapes and draw them in whatever place they are.
    def DrawShapes(self, dc):
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    # This is actually a sophisticated 'hit test', but in this
    # case we're also determining which shape, if any, was 'hit'.
    def FindShape(self, pt):
        for shape in reversed(self.shapes):
            if shape.HitTest(pt):
                return shape
        return None

    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.TileBackground(dc)

    # Fired whenever a paint event occurs
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self.DrawShapes(dc)

    # Left mouse button is down.
    def OnLeftDown(self, evt):
        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(evt.GetPosition())

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            self.dragShape = shape
            self.dragStartPos = evt.GetPosition()

    # Right mouse button is down.
    def OnRightDown(self, evt):
        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(evt.GetPosition())
        

        if shape:
            print "ok"
            self.delShape = shape

            if not hasattr(self, "popupID1"):
                self.popupID1 = wx.NewId()
                self.Bind(wx.EVT_MENU, self.DeleteShape, id=self.popupID1)            
            
            menu = wx.Menu()            
            menu.Append(self.popupID1, "Delete")
            self.PopupMenu(menu)
            menu.Destroy()


    def DrawLine(self):
        self.isDrawingLine = True
        self.lineCoordinates = []
        self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
            
    def DeleteShape(self, event):        
        dlg = wx.MessageDialog(self, 'Are you sure?',
                               'A Message Box',
                               #wx.OK | wx.ICON_INFORMATION
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                               )
        val = dlg.ShowModal()

        if val == wx.ID_YES:
            self.shapes.remove(self.delShape)
            self.board.postits.remove(self.delShape.postit)
            #self.delShape.delete(self.board)
            self.parent.Refresh()
            self.board.save()



        dlg.Destroy()
        

    # Left mouse button up.
    def OnLeftUp(self, evt):

        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None

            # Dibujar linea
            if self.isDrawingLine:
                if not self.lineCoordinates:
                    self.lineCoordinates = evt.GetPosition()
                else:
                    new_point = evt.GetPosition()
                    # Dibujar la linea a partir de los puntos
                    dc = wx.PaintDC(evt.GetEventObject())
                    #dc.Clear()
                    line = Line(self.lineCoordinates, new_point)
                    self.shapes.append(line)

                    # Agregar linea a board (kanban)
                    self.board.lines.append(line)

                    line.Draw(dc)
                    self.isDrawingLine = False
                    self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        if self.hiliteShape:
            self.RefreshRect(self.hiliteShape.GetRect())
            self.hiliteShape = None

        # reposition and draw the shape

        # Note by jmg 11/28/03 
        # Here's the original:
        #
        # self.dragShape.pos = self.dragShape.pos + evt.GetPosition() - self.dragStartPos
        #
        # So if there are any problems associated with this, use that as
        # a starting place in your investigation. I've tried to simulate the
        # wx.Point __add__ method here -- it won't work for tuples as we
        # have now from the various methods
        #
        # There must be a better way to do this :-)
        #
        self.shapes.remove(self.dragShape)
        self.board.postits.remove(self.dragShape.postit)
        self.shapes.append(self.dragShape)
        self.board.postits.append(self.dragShape.postit)   


        x = self.dragShape.pos[0] + evt.GetPosition()[0] - self.dragStartPos[0]
        y = self.dragShape.pos[1] + evt.GetPosition()[1] - self.dragStartPos[1]

        x = min(max(x,0), self.Size[0]-self.dragShape.postit.sizeX)
        y = min(max(y,0), self.Size[1]-self.dragShape.postit.sizeY)

        self.dragShape.pos = (x,y)

            
        self.dragShape.shown = True
        self.RefreshRect(self.dragShape.GetRect())
        self.dragShape.postit.moveTo(self.dragShape.pos[0], self.dragShape.pos[1])
        self.dragShape = None

        
             
        self.board.save()





        
        

    # The mouse is moving
    def OnMotion(self, evt):
        # Ignore mouse movement if we're not dragging.
        if not self.dragShape or not evt.Dragging() or not evt.LeftIsDown():
            return

        # if we have a shape, but haven't started dragging yet
        if self.dragShape and not self.dragImage:

            # only start the drag after having moved a couple pixels
            tolerance = 2
            pt = evt.GetPosition()
            dx = abs(pt.x - self.dragStartPos.x)
            dy = abs(pt.y - self.dragStartPos.y)
            if dx <= tolerance and dy <= tolerance:
                return

            # refresh the area of the window where the shape was so it
            # will get erased.
            self.dragShape.shown = False
            self.RefreshRect(self.dragShape.GetRect(), True)
            self.Update()

            if self.dragShape.text:
                self.dragImage = wx.DragString(self.dragShape.text,
                                              wx.StockCursor(wx.CURSOR_HAND))
            else:
                self.dragImage = wx.DragImage(self.dragShape.bmp,
                                             wx.StockCursor(wx.CURSOR_HAND))

            hotspot = self.dragStartPos - self.dragShape.pos
            self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

            self.dragImage.Move(pt)
            self.dragImage.Show()


        # if we have shape and image then move it, posibly highlighting another shape.
        elif self.dragShape and self.dragImage:

            self.parent.Refresh()

            onShape = self.FindShape(evt.GetPosition())
            unhiliteOld = False
            hiliteNew = False

            # figure out what to hilite and what to unhilite
            if self.hiliteShape:
                if onShape is None or self.hiliteShape is not onShape:
                    unhiliteOld = True

            if onShape and onShape is not self.hiliteShape and onShape.shown:
                hiliteNew = True

            # if needed, hide the drag image so we can update the window
            if unhiliteOld or hiliteNew:
                self.dragImage.Hide()

            if unhiliteOld:
                dc = wx.ClientDC(self)
                self.hiliteShape.Draw(dc)
                self.hiliteShape = None

            if hiliteNew:
                dc = wx.ClientDC(self)
                self.hiliteShape = onShape
                self.hiliteShape.Draw(dc, wx.INVERT)

            # now move it and show it again if needed
            new_position = []
            new_position += [min(max(evt.GetPosition()[0],0), self.Size[0])]
            new_position += [min(max(evt.GetPosition()[1],0), self.Size[1])]

            self.dragImage.Move(new_position)
            if unhiliteOld or hiliteNew:
                self.dragImage.Show()


#----------------------------------------------------------------------

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

#----------------------------------------------------------------------
