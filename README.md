La creación de nuevos ensayos es un proceso tedioso, debido a la configuración de la app, 
por ello vamos a crear una guía paso a paso, de como creamos el ensayo Explo/noExplo:

**IMPORTANTE LAS CLSASES LA PRIMERA EN AYUSCULA, LAS FUNCIONES LA PRIMERA EN MINÚSCULA**

1- Creamos el modelo en Ensayos y si es necesario el modelo de resultados de dichos ensayos.
2- Creamos el formulario del ensayo y el de resultados, si lleva formset lo actualizamos también
3- Creas la view
4- El template
5- Configuras las URL
6- Creas el ensayo en el admin
7- Asignar algún equipo desde la plataforma al ensayo
8- Creas el enlace en el layout de pages
9- Editamos el archivo signals, aquí mucha atención pues hay que modificar todo con el nombre del ensayo tal cual, para que no de errores.
10- Editamos en la view de muestras, listaEnsayosMuestra y listaEnsayosTerminados, incluyendo nuestros ensayos.
11- Añadimos el ensyo en generarPDF y plantillas de la carpeta PDF
