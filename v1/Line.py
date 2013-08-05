import wx
import math

#----------------------------------------------------------------------

def dist(p1, p2, p3):
    px = p2.x - p1.x
    py = p2.y - p1.y

    something = px*px + py*py

    u = ((p3.x - p1.x) * px + (p3.y - p1.y) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = p1.x + u * px
    y = p1.y + u * py

    dx = x - p3.x
    dy = y - p3.y

    distance = math.sqrt(dx*dx + dy*dy)

    return distance

# objeto que representa un post-it
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.shown = True

    # Recibe un punto e indica si esta dentro del rectangulo que contiene la imagen
    def HitTest(self, pt):

        pix_tol = 5

        """m = 1.0 * (self.p1.y - self.p2.y)/(self.p1.x - self.p2.x)
        a = -m
        b = 1
        dist = abs(a*pt.x + b*pt.y + (m*self.p2.x - self.p2.y))/((a**2+b**2)**0.5)"""

        distance = dist(self.p1, self.p2, pt)

        # m = 1

        # print "p1= ", self.p1, " p2= ", self.p2, " pt= ", pt, " m= ", m, " dist= " , distance

        return distance <= pix_tol

    # Retorna un rectangulo que contiene la imagen
    def GetRect(self):
        return wx.Rect(0, 0, 1, 1)

    def Draw(self, dc, op = wx.COPY):
        #dc = wx.PaintDC(evt.GetEventObject())
        #dc.Clear()
        dc.SetPen(wx.Pen("BLACK", 4))
        dc.DrawLine(self.p1[0], self.p1[1], self.p2[0], self.p2[1])

        return True

    def delete(self, kanban):
        kanban.lines.remove(self)
