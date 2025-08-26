import sys
from collections import deque

def solve():
    """
    Resuelve el problema "Expanding STACKS!" modelándolo como un problema de
    2-coloración de grafos (comprobación de bipartición).
    """
    try:
        n = int(sys.stdin.readline())
        events = list(map(int, sys.stdin.readline().split()))
    except (IOError, ValueError):
        return

    # --- PASO 1: Pre-procesamiento para encontrar los intervalos de vida ---
    # Guardamos el "tiempo" (índice en la lista de eventos) de entrada y salida.
    entry_time = [0] * (n + 1)
    leave_time = [0] * (n + 1)
    for i, event in enumerate(events):
        customer_id = abs(event)
        if event > 0:
            entry_time[customer_id] = i
        else:
            leave_time[customer_id] = i

    # --- PASO 2: Construcción del grafo de conflictos ---
    # Creamos una arista entre dos clientes si deben estar en filas diferentes.
    adj = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            # Comprobamos si los intervalos de vida de i y j se entrelazan.
            # Ordenamos los intervalos por su tiempo de entrada para simplificar la lógica.
            e1, l1 = entry_time[i], leave_time[i]
            e2, l2 = entry_time[j], leave_time[j]

            if e1 > e2:
                e1, l1, e2, l2 = e2, l2, e1, l1 # Asegura que el cliente 1 entró primero

            # La condición de entrelazado: el primero entra, el segundo entra,
            # el primero sale, el segundo sale.
            if e1 < e2 and e2 < l1 and l1 < l2:
                # Si se entrelazan, no pueden estar en la misma fila (pila).
                # Creamos una arista para representar esta restricción.
                adj[i].append(j)
                adj[j].append(i)

    # --- PASO 3: 2-Coloración del grafo usando BFS ---
    # 0: sin color, 1: 'G', 2: 'S'
    colors = [0] * (n + 1)
    is_possible = True

    for i in range(1, n + 1):
        # Si este nodo (componente del grafo) aún no ha sido visitado/coloreado
        if colors[i] == 0:
            colors[i] = 1  # Empezamos asignando el primer color
            q = deque([i])

            while q:
                u = q.popleft()
                
                # Para cada vecino del nodo actual
                for v in adj[u]:
                    if colors[v] == 0:
                        # Si el vecino no tiene color, le damos el opuesto
                        colors[v] = 3 - colors[u] # (3-1=2, 3-2=1)
                        q.append(v)
                    elif colors[v] == colors[u]:
                        # Si el vecino tiene el MISMO color, hay un conflicto.
                        # Esto significa que el grafo no es bipartito.
                        is_possible = False
                        break
                if not is_possible:
                    break
        if not is_possible:
            break
            
    # --- PASO 4: Salida del resultado ---
    if not is_possible:
        print("*")
    else:
        result_string = ""
        for i in range(1, n + 1):
            # Si a un cliente nunca se le asignó un color (porque no tenía conflictos
            # con nadie), podemos asignarle 'G' por defecto.
            if colors[i] == 1 or colors[i] == 0:
                result_string += "G"
            else:
                result_string += "S"
        print(result_string)


solve()