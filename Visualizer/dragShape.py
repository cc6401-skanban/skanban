
#----------------------------------------------------------------------

# objeto que representa un post-it
class DragShape:
    def __init__(self, bmp):
        self.bmp = bmp	 					# image
        self.pos = (0,0)					# posicion superior izquierda, se inicia en 0,0
        self.shown = True					# define si es visible
        self.text = None					# si no es none la imagen es reemplazada por el texto cuando se arrastra
        self.fullscreen = False				# define si la imagen puede arrastrarse fuera de la ventana
        self.postit = None

    # Recibe un punto e indica si esta dentro del rectangulo que contiene la imagen
    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    # Retorna un rectangulo que contiene la imagen
    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            # se pide memoria para almacenar el bmp
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False

