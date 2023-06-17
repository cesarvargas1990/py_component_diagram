# Generador de diagramas de componentes
Crea un diagrama de componentes leyendo un json
# Requisitos
## Python3
## Libreria graphviz
 instálala usando `pip install graphviz`
 ## Ejemplo de estructura
 Modificar archivo `servicios.json` de acuerdo a sus requerimientos
 ## Ejecutar 
 `python3 component_diagram_generator.py`
 ## Nota
 En algunas ocasiones no tiene en cuenta bien la configuracion del json y genera algunos componentes "juntos" que tienen conexion y estan separados, esto se soluciona ejecutando nuevamente el comando:  `python3 component_diagram_generator.py`
