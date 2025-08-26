import sys

def calculate_area(t, X, Y, Vx, Vy, n):
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for i in range(n):
        px = X[i] + t * Vx[i]
        py = Y[i] + t * Vy[i]
        min_x = min(min_x, px)
        max_x = max(max_x, px)
        min_y = min(min_y, py)
        max_y = max(max_y, py)
    return (max_x - min_x) * (max_y - min_y)

def calculate_width(t, X, Vx, n):
    min_x, max_x = float('inf'), float('-inf')
    for i in range(n):
        px = X[i] + t * Vx[i]
        min_x = min(min_x, px)
        max_x = max(max_x, px)
    return max_x - min_x

def calculate_height(t, Y, Vy, n):
    min_y, max_y = float('inf'), float('-inf')
    for i in range(n):
        py = Y[i] + t * Vy[i]
        min_y = min(min_y, py)
        max_y = max(max_y, py)
    return max_y - min_y

def solve():
    try:
        n_str = sys.stdin.readline()
        if not n_str: return
        N = int(n_str)
        X, Y, Vx, Vy = [], [], [], []
        for _ in range(N):
            x, y, vx, vy = map(int, sys.stdin.readline().split())
            X.append(float(x))
            Y.append(float(y))
            Vx.append(float(vx))
            Vy.append(float(vy))
    except (IOError, ValueError):
        return

    # Paso 1: Encontrar t_x que minimiza el Ancho
    low_x, high_x = 0.0, 2e9
    for _ in range(100):
        m1 = low_x + (high_x - low_x) / 3
        m2 = high_x - (high_x - low_x) / 3
        if calculate_width(m1, X, Vx, N) < calculate_width(m2, X, Vx, N):
            high_x = m2
        else:
            low_x = m1
    optimal_t_x = (low_x + high_x) / 2

    # Paso 2: Encontrar t_y que minimiza el Alto
    low_y, high_y = 0.0, 2e9
    for _ in range(100):
        m1 = low_y + (high_y - low_y) / 3
        m2 = high_y - (high_y - low_y) / 3
        if calculate_height(m1, Y, Vy, N) < calculate_height(m2, Y, Vy, N):
            high_y = m2
        else:
            low_y = m1
    optimal_t_y = (low_y + high_y) / 2

    # Paso 3: Búsqueda ternaria del Área en el rango [t_x, t_y]
    final_low = min(optimal_t_x, optimal_t_y)
    final_high = max(optimal_t_x, optimal_t_y)
    
    # Aseguramos que el rango de búsqueda no sea inválido
    if final_low > final_high:
        final_low, final_high = final_high, final_low
        
    for _ in range(100):
        m1 = final_low + (final_high - final_low) / 3
        m2 = final_high - (final_high - final_low) / 3
        if calculate_area(m1, X, Y, Vx, Vy, N) < calculate_area(m2, X, Y, Vx, Vy, N):
            final_high = m2
        else:
            final_low = m1

    optimal_t = (final_low + final_high) / 2
    min_area_search = calculate_area(optimal_t, X, Y, Vx, Vy, N)
    
    # Comprobar t=0 explícitamente
    area_at_zero = calculate_area(0, X, Y, Vx, Vy, N)

    min_area = min(min_area_search, area_at_zero)
    
    print(f"{min_area:.15f}")

solve()