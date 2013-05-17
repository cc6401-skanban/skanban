import sys
import wx
import DragCanvas

def main():

    if len(sys.argv) < 5:
        print "Debe indicar los siguientes parametros: anchoVentanaPrincipal altoVentanaPrincipal  imagenFondo imagenes[]."
        raise SystemExit
    
    print "Ancho de ventana: " + sys.argv[1] + " px."
    print "Alto de ventana: " + sys.argv[2] + " px." 
    print "Imagen de fondo: " + sys.argv[3]

    for x in range(len(sys.argv)):
        if x > 3:
            print "Imagen ",(x - 3), " : " + sys.argv[x]

    app = wx.PySimpleApp()
	
    frame = wx.Frame(None, -1, "Skanban 2013 | CC6401 ", pos=(50,50), size=(int(sys.argv[1]),int(sys.argv[2])), style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
    # sys.argv[3] es la imagen de fondo, los argumentos posteriores son las imagenes
    dc = DragCanvas.DragCanvas(frame,-1, sys.argv[3], sys.argv[4:])
    frame.Show(1)
	
    app.MainLoop()
	

if __name__ == "__main__":
    main()