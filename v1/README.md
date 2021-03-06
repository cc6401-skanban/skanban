Instrucciones de Uso
======
Esta aplicación tiene por objetivo manipular mapas mentales a partir de una foto. Su algoritmo consiste en detectar los post-its o cuadrados marcados en la foto, recortarlos y manipularlos independientemente, permitiendo moverlos, y también agregar lineas, texto o color de fondo al mapa. Esto vuelve al mapa portable, ya que se pueden exportar archivos .skb, para poder compartir los mapas.
Se recomienda utilizar fotos donde los postits se vean bien definidos, y que no haya superposición de éstos. Si existen errores, los post-its pueden borrarse y agregarse manualmente al mapa digital.
Si utiliza el software, por favor enviarnos feedback a cc6401-equipo-skanban@googlegroups.com

<h2>Requisitos del Sistema</h2>

La aplicación Skanban v1.0 requiere tener instalados en su sistema operativo (Windows, Linux o OS X), los siguientes módulos:
- Python 2.7.
- OpenCV 2.4.5 o superior.
- WXPython 2.8
- Numpy 1.7.1


<h2>Modo de Uso</h2>

Para correr la aplicación, se debe: 

- Descomprimir la aplicación 
- Ejecutar el arhivo Skanban.py, pasando como parámetro la imagen que se desea utilizar en el software.

Ejemplo Linux:

  <b>user@system:~/Skanban$</b> python Skanban.py imagen.jpg
  
Ejemplo Windows:

  <b>C:\User\Skanban></b> python Skanban.py imagen.jpg


<h2>Funcionalidades</h2>

Dentro del sistema encontrará un menú superior que le permitirá realizar las siguientes acciones:

<b>Nuevo:</b> Esta opción le permite seleccionar una imagen para generar un nuevo kanban virtual.

<b>Guardar:</b> Esta opción le permite guardar el estado actual del kanban virtual a un archivo portable.

<b>Cargar:</b> Esta opción le permite abrir un archivo portable previamente guardado.


<b>Agregar post-it:</b> Esta opción le permite re-abrir la foto original para incorporar un nuevo post-it que pudiera no haber sido detectado. Para ello, al abrirse la foto original, usted debe seleccionar los cuatro puntos de las esquinas del post-it a agregar. Esto automáticamente hará aparecer el post-it en la ventana de kanban virtual.

<b>Cambiar color fondo:</b> Esta opción abrirá una paleta de colores que le permitirá seleccionar un nuevo color de fondo para la ventana de kanban virtual.

<b>Agregar Linea:</b> Esta opción abrirá una paleta de colores que le permitirá seleccionar un nuevo color de fondo para la ventana de kanban virtual.

<b>Agregar Texto:</b> Esta opción permite insertar un texto en el mapa mental..

<b>Ver foto original:</b> Esta opción muestra en escala de grises la foto original utilizada.

<b>Acerca de:</b> Aquí encontrará información sobre la licencia del Software, sobre el equipo de Desarrollo y podrá conocer la versión del software que está utilizando.
