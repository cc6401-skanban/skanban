#!/usr/bin/env python
import wx
import sys
import  cStringIO

class Panel1(wx.Panel):
  """ class Panel1 creates a panel with an image on it, inherits wx.Panel """
  def __init__(self, parent, id, imageFile):
    # create the panel
    wx.Panel.__init__(self, parent, id)
    try:
        # alternate (simpler) way to load and display a jpg image from a file
        # actually you can load .jpg  .png  .bmp  or .gif files
        jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
        wx.StaticBitmap(self, -1, jpg1, (0,0), (jpg1.GetWidth(), jpg1.GetHeight()))
    except IOError:
        print "Image file %s not found" % imageFile
        raise SystemExit

app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
# increase the size of the frame for larger images
imageFile = sys.argv[1]
jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

frame1 = wx.Frame(None, -1, "An image on a panel", size = (jpg1.GetWidth(), jpg1.GetHeight()))
# call the derived class
Panel1(frame1,-1, sys.argv[1])
frame1.Show(1)
app.MainLoop()


