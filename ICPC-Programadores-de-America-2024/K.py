import sys
import heapq

def solve():
    try:
        n_str = sys.stdin.readline()
        if not n_str: return
        N = int(n_str)
        words = [sys.stdin.readline().strip() for _ in range(N)]
    except (IOError, ValueError):
        return

    # --- LA CORRECCIÓN CLAVE ESTÁ AQUÍ ---
    vowels = "AEIOUY" 

    # dist[i][j]: longitud minima del acronimo usando las primeras i palabras,
    # terminando con j consonantes.
    dist = [[float('inf')] * 3 for _ in range(N)]
    
    # Cola de prioridad para Dijkstra: (longitud, palabra_idx, cons_finales)
    pq = []

    # --- Casos Base (primera palabra, i=0) ---
    for length in range(1, min(len(words[0]), 3) + 1):
        prefix = words[0][:length]
        
        consonants = 0
        valid = True
        for char in prefix:
            if char not in vowels:
                consonants += 1
                if consonants > 2:
                    valid = False
                    break
            else:
                consonants = 0
        
        if valid:
            if length < dist[0][consonants]:
                dist[0][consonants] = length
                heapq.heappush(pq, (length, 0, consonants))

    # --- Dijkstra en el grafo de estados ---
    while pq:
        current_len, word_idx, last_cons = heapq.heappop(pq)

        if current_len > dist[word_idx][last_cons]:
            continue

        if word_idx == N - 1:
            continue

        next_word_idx = word_idx + 1
        for length in range(1, min(len(words[next_word_idx]), 3) + 1):
            prefix = words[next_word_idx][:length]
            
            temp_cons = last_cons
            valid_transition = True
            for char in prefix:
                if char not in vowels:
                    temp_cons += 1
                else:
                    temp_cons = 0
                
                if temp_cons > 2:
                    valid_transition = False
                    break
            
            if valid_transition:
                new_len = current_len + length
                if new_len < dist[next_word_idx][temp_cons]:
                    dist[next_word_idx][temp_cons] = new_len
                    heapq.heappush(pq, (new_len, next_word_idx, temp_cons))

    # --- Respuesta Final ---
    result = min(dist[N-1])
    
    if result == float('inf'):
        print("*")
    else:
        print(result)

solve()