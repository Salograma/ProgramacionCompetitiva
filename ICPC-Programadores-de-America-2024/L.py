import sys

def solve():
    """
    Función principal para resolver el problema.
    """
    try:
        # --- Lectura de la entrada ---
        # Leemos las dimensiones R, C, K
        r, c, k = map(int, sys.stdin.readline().split())
        
        # Variable para llevar el resultado. Asumimos que es posible ('Y')
        # hasta que encontremos una contradicción.
        is_possible = True
        
        # --- Lógica Principal: Procesar fila por fila ---
        for _ in range(r):
            # Leemos la fila de la matriz y la del patrón.
            # El .split() por defecto maneja el espacio entre M y P.
            matrix_row, pattern_row = sys.stdin.readline().strip().split()
            
            # --- La Condición Crítica ---
            # ¿Hay algún LED roto en esta fila de la matriz?
            has_broken_leds = '-' in matrix_row
            
            # ¿El patrón necesita encender algún LED en esta fila?
            pattern_needs_on = '*' in pattern_row
            
            # Si hay un LED roto Y el patrón necesita encender algo en esta fila, es imposible.
            if has_broken_leds and pattern_needs_on:
                is_possible = False
                # No podemos hacer un 'break' o 'return' aquí, porque necesitamos
                # seguir leyendo las líneas restantes de la entrada para no
                # desincronizar la lectura en caso de múltiples casos de prueba
                # (aunque este problema solo tenga uno, es una buena práctica).

    except (IOError, ValueError):
        # Manejo de errores de lectura o final de archivo
        return

    # --- Salida ---
    # Imprimimos el resultado final después de haber procesado todas las filas.
    if is_possible:
        print("Y")
    else:
        print("N")

# Llamamos a la función para ejecutar la solución.
solve()