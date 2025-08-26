import sys
from collections import deque

def solve():
    # ====================================================================================
    # PASO 0: RECONOCER EL PATRÓN - ¿POR QUÉ ESTO ES UN PROBLEMA DE GRAFOS?
    # ====================================================================================
    #
    # 1. IDENTIFICAR LA RESTRICCIÓN CLAVE:
    #    La regla del restaurante es "Last-In, First-Out" (LIFO). Esto es, por definición,
    #    el comportamiento de una ESTRUCTURA DE DATOS DE PILA (STACK).
    #    Tenemos dos filas, Glaseada (G) y Salada (S), por lo tanto, tenemos dos pilas.
    #
    # 2. ANALIZAR LA CONDICIÓN DE FALLO:
    #    Una asignación falla si un cliente 'i' debe salir, pero otro cliente 'j' que
    #    entró después que 'i' está encima de él en la misma pila.
    #    Ejemplo de fallo:
    #    - Entra 'i' -> Pila G: [i]
    #    - Entra 'j' -> Pila G: [i, j]
    #    - Sale 'i'  -> ¡ERROR! La cima de la pila es 'j', no 'i'.
    #
    # 3. TRADUCIR LA CONDICIÓN DE FALLO A UNA RELACIÓN:
    #    El escenario de fallo anterior ocurre si y solo si los "intervalos de vida"
    #    de los clientes 'i' y 'j' se entrelazan. Un intervalo de vida es el tiempo
    #    desde que un cliente entra hasta que sale.
    #    Entrelazado significa: entra(i) < entra(j) < sale(i) < sale(j).
    #
    # 4. FORMULAR LA RESTRICCIÓN EN TÉRMINOS SIMPLES:
    #    "SI los intervalos de 'i' y 'j' se entrelazan, ENTONCES 'i' y 'j' NO PUEDEN
    #     estar en la misma pila".
    #    Esto es una restricción de diferencia: i != j (en términos de pila/fila).
    #
    # 5. HACER LA CONEXIÓN CON LA TEORÍA DE GRAFOS:
    #    Un problema donde tienes un conjunto de elementos (clientes) y una serie de
    #    restricciones de "estos dos deben ser diferentes" es un problema clásico de
    #    COLORACIÓN DE GRAFOS.
    #    - Los NODOS del grafo son los elementos (los clientes).
    #    - Una ARISTA entre dos nodos 'i' y 'j' representa la restricción "i y j deben
    #      ser diferentes".
    #    - Los "COLORES" son las opciones que podemos asignar (las filas 'G' y 'S').
    #
    # 6. IDENTIFICAR EL TIPO ESPECÍFICO DE PROBLEMA DE GRAFOS:
    #    Como solo tenemos dos "colores" ('G' y 'S'), este es un problema de 2-COLORACIÓN.
    #    Un grafo se puede 2-colorear si y solo si es BIPARTITO (no contiene ciclos
    #    de longitud impar).
    #
    # 7. RESUMEN DEL PLAN DE ACCIÓN:
    #    a) Determinar los intervalos de vida de cada cliente.
    #    b) Construir un grafo donde una arista (i, j) significa que sus intervalos se entrelazan.
    #    c) Comprobar si este grafo es bipartito usando un algoritmo de 2-coloración (como BFS o DFS).
    #    d) Si es bipartito, la coloración nos da una asignación válida. Si no, no hay solución.
    #
    # ====================================================================================

    try:
        n = int(sys.stdin.readline())
        events = list(map(int, sys.stdin.readline().split()))
    except (IOError, ValueError):
        return

    # --- PASO DE PROGRAMACIÓN 1: Pre-procesamiento de Intervalos ---
    # Para construir el grafo, necesitamos saber cuándo entró y salió cada cliente.
    # Usamos dos arrays para almacenar el "tiempo" (que es el índice en la lista de eventos).
    entry_time = [0] * (n + 1)
    leave_time = [0] * (n + 1)
    for i, event in enumerate(events):
        customer_id = abs(event)
        if event > 0:
            entry_time[customer_id] = i
        else:
            leave_time[customer_id] = i

    # --- PASO DE PROGRAMACIÓN 2: Construcción del Grafo de Conflictos ---
    # Creamos una lista de adyacencia para representar el grafo.
    # 'adj[i]' contendrá una lista de todos los clientes que tienen un conflicto con 'i'.
    adj = [[] for _ in range(n + 1)]
    # Iteramos sobre todos los pares posibles de clientes (i, j) para buscar conflictos.
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            # Obtenemos los tiempos de entrada y salida para el par (i, j).
            e1, l1 = entry_time[i], leave_time[i]
            e2, l2 = entry_time[j], leave_time[j]

            # Definimos la condición de entrelazado:
            # (e1 < e2 < l1 < l2) O (e2 < e1 < l2 < l1)
            # Esto significa que uno entra, el otro entra, el primero sale, y luego el segundo sale.
            # Esta es la única configuración que crea un conflicto de pila.
            is_interleaved = (e1 < e2 and e2 < l1 and l1 < l2) or \
                             (e2 < e1 and e1 < l2 and l2 < l1)
            
            if is_interleaved:
                # Si hay un conflicto, añadimos una arista entre ellos.
                # El grafo es no dirigido, así que añadimos la arista en ambas direcciones.
                adj[i].append(j)
                adj[j].append(i)

    # --- PASO DE PROGRAMACIÓN 3: Algoritmo de 2-Coloración (Bipartite Checking) ---
    # Usaremos una Búsqueda en Anchura (BFS) para colorear el grafo.
    # 'colors' almacenará el color de cada nodo. Usaremos números para la lógica:
    # 0: sin color (no visitado)
    # 1: color 'G'
    # 2: color 'S'
    colors = [0] * (n + 1)
    is_possible = True # Una bandera para detenernos si encontramos un conflicto.

    # Debemos iterar por todos los nodos, porque el grafo puede tener múltiples
    # componentes conexas (grupos de clientes que no interactúan entre sí).
    for i in range(1, n + 1):
        # Si el nodo 'i' no ha sido coloreado, iniciamos un nuevo BFS desde él.
        if colors[i] == 0:
            colors[i] = 1  # Le asignamos el primer color ('G')
            q = deque([i]) # Creamos una cola para el BFS

            while q:
                u = q.popleft() # Tomamos un nodo de la cola
                
                # Exploramos todos sus vecinos
                for v in adj[u]:
                    if colors[v] == 0:
                        # Si el vecino no tiene color, le damos el color opuesto al de 'u'.
                        colors[v] = 3 - colors[u] # (3-1=2, 3-2=1) es un truco para alternar.
                        q.append(v)
                    elif colors[v] == colors[u]:
                        # ¡CONFLICTO! 'v' ya tiene color, y es el MISMO que 'u'.
                        # Pero como hay una arista entre ellos, deberían tener colores DIFERENTES.
                        # Esto significa que hemos encontrado un ciclo de longitud impar.
                        # El grafo no es bipartito y no hay solución.
                        is_possible = False
                        break
                if not is_possible:
                    break
        if not is_possible:
            break
            
    # --- PASO DE PROGRAMACIÓN 4: Construir y Mostrar la Salida ---
    if not is_possible:
        # Si en algún momento encontramos un conflicto, la respuesta es imposible.
        print("*")
    else:
        # Si el bucle terminó sin conflictos, hemos encontrado una coloración válida.
        result_string = ""
        for i in range(1, n + 1):
            # Convertimos nuestra representación numérica de colores a 'G' y 'S'.
            # Si un nodo no tiene color (colors[i] == 0), significa que no tenía
            # conflictos con nadie (es un nodo aislado). Podemos asignarle
            # cualquier color, por ejemplo 'G'.
            if colors[i] == 1 or colors[i] == 0:
                result_string += "G"
            else: # colors[i] == 2
                result_string += "S"
        print(result_string)


solve()