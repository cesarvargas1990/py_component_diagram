import json
from graphviz import Digraph

def generate_component_diagram(json_file, output_diagram_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Obtener la configuración de las zonas
    zone_config = data.get('config', {})
    space_between_zones = zone_config.get('espacio_entre_zonas', '0.5')

    # Crear el objeto Digraph
    graph = Digraph(format='png', graph_attr={'rankdir': 'LR', 'nodesep': space_between_zones})

    zones = data.get('zonas', [])

    # Recorrer las zonas
    for zone in zones:
        zone_name = zone.get('nombre')
        zone_color = zone.get('color', '#FFFFFF')  # Color por defecto: blanco

        # Crear un subgrafo para la zona
        with graph.subgraph(name=f'cluster_{zone_name}') as subgraph:
            subgraph.attr(style='filled', color=zone_color)
            subgraph.attr(label=zone_name)

            services = zone.get('servicios', [])
            boxes = zone.get('cuadros', [])

            # Agregar los servicios de la zona
            for service in services:
                service_name = service.get('nombre')
                service_port = service.get('puerto')
                service_color = service.get('color', 'lightgray')  # Color por defecto: lightgray
                service_font_color = service.get('color_fuente', 'black')  # Color por defecto: negro

            
                subgraph.node(service_name, label=f'{service_name}\nPort: {service_port}', style='filled', fillcolor=service_color, fontcolor=service_font_color)

                connections = service.get('conexiones', [])

                # Agregar las conexiones del servicio
                for connection in connections:
                    # Comprobar si la conexión es bidireccional
                    if (
                        connection in services
                        and service_name in services[connection].get('conexiones', [])
                    ):
                        # Conexión bidireccional: agregar una línea con flechas en ambas puntas
                        subgraph.edge(service_name, connection, dir='both', arrowhead='normal', arrowtail='normal')
                        # Remover la conexión del servicio conectado para evitar una conexión duplicada
                        services[connection]['conexiones'].remove(service_name)
                    else:
                        # Conexión unidireccional: agregar una flecha
                        subgraph.edge(service_name, connection)

            # Agregar los cuadros de la zona
            for box in boxes:
                box_name = box.get('nombre')
                box_services = box.get('servicios', [])
                box_color = box.get('color', 'lightgray')  # Color por defecto: lightgray

                # Crear un subgrafo para el cuadro dentro de la zona
                with subgraph.subgraph(name=f'cluster_{zone_name}_{box_name}') as box_subgraph:
                    box_subgraph.attr(style='filled', color=box_color)
                    box_subgraph.attr(label=box_name)

                    # Agregar los servicios dentro del cuadro
                    for box_service in box_services:
                        box_service_name = box_service.get('nombre')
                        box_service_port = box_service.get('puerto')
                        box_service_color = box_service.get('color', 'lightgray')  # Color por defecto: lightgray
                        box_service_font_color = box_service.get('color_fuente', 'black')  # Color por defecto: negro

                        # Agregar el servicio como un cuadro al subgrafo del cuadro
                        box_subgraph.node(box_service_name, shape='box', label=f'{box_service_name}\nPort: {box_service_port}', style='filled', fillcolor=box_service_color, fontcolor=box_service_font_color)

                        box_connections = box_service.get('conexiones', [])

                        # Agregar las conexiones del servicio dentro del cuadro
                        for box_connection in box_connections:
                            # Comprobar si la conexión está dentro del cuadro
                            if box_connection in box_services:
                                # Conexión dentro del cuadro: agregar una flecha
                                box_subgraph.edge(box_service_name, box_connection)
                            else:
                                # Conexión fuera del cuadro: agregar una flecha al subgrafo de la zona principal
                                graph.edge(box_service_name, box_connection)

    # Renderizar el diagrama y guardarlo en un archivo
    graph.render(output_diagram_file, view=True)

# Ejemplo de uso
json_file = 'servicios.json'
output_diagram_file = 'component_diagram'
generate_component_diagram(json_file, output_diagram_file)
