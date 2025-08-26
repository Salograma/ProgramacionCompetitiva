import sys

def solve():
    """
    Resuelve el problema 'Joys of Trading' usando un algoritmo greedy
    basado en el principio económico de ventaja comparativa.
    """
    try:
        # --- LECTURA DE ENTRADA ---
        n_str = sys.stdin.readline()
        if not n_str: return
        n = int(n_str)
    except (IOError, ValueError):
        return

    # --- PASO 1: CLASIFICACIÓN Y CÁLCULO INICIAL ---
    # La idea es clasificar los recursos en tres grupos:
    # 1. group_a: Apolynka es más eficiente (A_i < B_i)
    # 2. group_b: Büdelsdorf es más eficiente (B_i < A_i)
    # 3. Costo igual: No importa quién lo produzca, el costo es fijo.
    group_a = []
    group_b = []

    total_cost = 0.0
    capacity_a = 0.0  # Capacidad total de trabajo de Apolynka (su "presupuesto")
    capacity_b = 0.0  # Capacidad total de trabajo de Büdelsdorf

    for _ in range(n):
        a, u, b, w = map(int, sys.stdin.readline().split())
        
        # Calculamos la capacidad de trabajo original, que actúa como nuestro "presupuesto"
        capacity_a += a * u
        capacity_b += b * w
        
        total_production = u + w
        
        if a < b:
            group_a.append({'prod': total_production, 'cost_a': a, 'cost_b': b})
        elif b < a:
            group_b.append({'prod': total_production, 'cost_a': a, 'cost_b': b})
        else:
            # Si el costo es igual, la decisión no afecta la optimización.
            # Añadimos su costo fijo al total inmediatamente.
            total_cost += total_production * a

    # --- PASO 2: CÁLCULO DEL ESCENARIO "IDEAL" ---
    # Asumimos que cada aldea se especializa completamente en lo que hace mejor.
    # Este es el costo mínimo teórico, pero podría no ser factible.
    required_a = sum(r['prod'] * r['cost_a'] for r in group_a)
    required_b = sum(r['prod'] * r['cost_b'] for r in group_b)
    
    # El costo total ideal es la suma de los costos fijos y los costos de especialización.
    total_cost += required_a + required_b
    
    # --- PASO 3 y 4: REEQUILIBRIO GREEDY SI HAY SOBRECARGA ---
    # Comprobamos si la asignación ideal excede la capacidad de alguna aldea.
    if required_a > capacity_a:
        # Apolynka está sobrecargada. Debe ceder trabajo.
        overload_hours = required_a - capacity_a
        
        # DECISIÓN GREEDY CRUCIAL: ¿Qué trabajo ceder primero?
        # Cedemos el trabajo que es "menos valioso" para Apolynka, es decir,
        # aquel donde su ventaja por hora de trabajo es la más pequeña.
        # Esto es equivalente a ordenar por la "penalización por hora" que se paga
        # al ceder el trabajo: (B_i - A_i) / A_i.
        group_a.sort(key=lambda r: (r['cost_b'] - r['cost_a']) / r['cost_a'])
        
        # --- PASO 5: APLICAR EL REEQUILIBRIO ---
        for res in group_a:
            if overload_hours <= 0: break
            
            hours_a_for_this_task = res['prod'] * res['cost_a']
            penalty_per_hour = (res['cost_b'] - res['cost_a']) / res['cost_a']
            
            # Determinamos cuántas horas de trabajo ceder de esta tarea.
            # Es el mínimo entre lo que queda de sobrecarga y el total de la tarea.
            hours_to_offload = min(overload_hours, hours_a_for_this_task)
            
            # Añadimos el costo extra (la penalización) al costo total.
            total_cost += hours_to_offload * penalty_per_hour
            overload_hours -= hours_to_offload
                
    elif required_b > capacity_b:
        # El caso simétrico: Büdelsdorf está sobrecargado.
        overload_hours = required_b - capacity_b
        
        # Ordenamos por la penalización por hora para Büdelsdorf: (A_i - B_i) / B_i
        group_b.sort(key=lambda r: (r['cost_a'] - r['cost_b']) / r['cost_b'])
        
        for res in group_b:
            if overload_hours <= 0: break
            
            hours_b_for_this_task = res['prod'] * res['cost_b']
            penalty_per_hour = (res['cost_a'] - res['cost_b']) / res['cost_b']
            
            hours_to_offload = min(overload_hours, hours_b_for_this_task)
            
            total_cost += hours_to_offload * penalty_per_hour
            overload_hours -= hours_to_offload
                
    # --- SALIDA ---
    print(f"{total_cost:.12f}")

solve()