import wx

#----------------------------------------------------------------------

# objeto que representa un post-it
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.shown = True

    # Recibe un punto e indica si esta dentro del rectangulo que contiene la imagen
    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    # Retorna un rectangulo que contiene la imagen
    def GetRect(self):
        return wx.Rect(0, 0, 1, 1)

    def Draw(self, dc, op = wx.COPY):
        #dc = wx.PaintDC(evt.GetEventObject())
        #dc.Clear()
        dc.SetPen(wx.Pen("BLACK", 4))
        dc.DrawLine(self.p1[0], self.p1[1], self.p2[0], self.p2[1])

        return True
