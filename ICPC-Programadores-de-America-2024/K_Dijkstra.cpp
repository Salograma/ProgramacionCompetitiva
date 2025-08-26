#include <iostream>   // Para entrada/salida (cin, cout)
#include <vector>     // Para usar std::vector (arreglos dinámicos)
#include <string>     // Para usar std::string
#include <queue>      // Para usar std::priority_queue (el heap)
#include <algorithm>  // Para usar std::min

// ====================================================================================
// PROCESO DE PENSAMIENTO Y ESTRATEGIA
// ====================================================================================
// PASO 0: DIAGNÓSTICO
// El problema pide la "longitud mínima" de un acrónimo, construido secuencialmente.
// Esto se puede modelar como un problema de encontrar el CAMINO MÁS CORTO en un grafo.
//
// PASO 1: MODELADO DEL GRAFO DE ESTADOS
// - NODOS: Un estado se define por (índice_de_palabra, consonantes_finales).
// - ARISTAS: Una arista es una transición de (i, j_prev) a (i+1, j_nuevo)
//            al elegir un prefijo de la palabra i+1.
// - PESOS: El peso de una arista es la longitud del prefijo elegido.
//
// PASO 2: ELECCIÓN DEL ALGORITMO
// Como es un problema de camino más corto con pesos no negativos (1, 2, 3),
// el algoritmo perfecto es DIJKSTRA. Usaremos una cola de prioridad para
// explorar siempre el camino de menor longitud acumulada primero.
// ====================================================================================

// Se define una constante para representar un valor "infinito".
const int INF = 1e9;

// Función auxiliar para determinar si un carácter es una vocal.
bool is_vowel(char c) {
    return c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U' || c == 'Y';
}

void solve() {
    // --- Lectura de la entrada ---
    int n;
    std::cin >> n;
    std::vector<std::string> words(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> words[i];
    }

    // --- Inicialización de Dijkstra ---
    // dist[i][j]: longitud mínima para un acrónimo con las primeras i+1 palabras,
    // terminando con j consonantes.
    std::vector<std::vector<int>> dist(n, std::vector<int>(3, INF));

    // Cola de prioridad: { -longitud, {palabra_idx, cons_finales} }
    // Se usa longitud negativa porque std::priority_queue es un max-heap por defecto.
    // Al negar, el valor más grande (menos negativo) corresponde a la longitud más corta.
    std::priority_queue<std::pair<int, std::pair<int, int>>> pq;

    // --- Paso 1: Casos Base (procesar la primera palabra, i=0) ---
    // Se calculan los estados iniciales y se añaden a la cola de prioridad.
    for (int len = 1; len <= std::min((int)words[0].length(), 3); ++len) {
        std::string prefix = words[0].substr(0, len);
        
        int consonants = 0;
        bool valid = true;
        for (char c : prefix) {
            if (!is_vowel(c)) {
                consonants++;
            } else {
                consonants = 0;
            }
            if (consonants > 2) {
                valid = false;
                break;
            }
        }
        
        if (valid) {
            if (len < dist[0][consonants]) {
                dist[0][consonants] = len;
                pq.push({-len, {0, consonants}});
            }
        }
    }

    // --- Paso 2: Dijkstra en el grafo de estados ---
    while (!pq.empty()) {
        // Extraer el estado con la menor longitud acumulada.
        int current_len = -pq.top().first;
        int word_idx = pq.top().second.first;
        int last_cons = pq.top().second.second;
        pq.pop();

        // Optimización: si ya encontramos un camino más corto a este estado, ignoramos este.
        if (current_len > dist[word_idx][last_cons]) {
            continue;
        }

        // Si ya estamos en la última palabra, no podemos generar más transiciones.
        if (word_idx == n - 1) {
            continue;
        }

        // Se exploran las "aristas" hacia los estados de la siguiente palabra.
        int next_word_idx = word_idx + 1;
        for (int len = 1; len <= std::min((int)words[next_word_idx].length(), 3); ++len) {
            std::string prefix = words[next_word_idx].substr(0, len);
            
            // Se simula la concatenación para verificar la validez de la transición.
            int temp_cons = last_cons;
            bool valid_transition = true;
            for (char c : prefix) {
                if (!is_vowel(c)) {
                    temp_cons++;
                } else {
                    temp_cons = 0;
                }
                if (temp_cons > 2) {
                    valid_transition = false;
                    break;
                }
            }
            
            // Si la transición es válida, "relajamos la arista".
            if (valid_transition) {
                int new_len = current_len + len;
                // Si encontramos un camino más corto al nuevo estado, lo actualizamos.
                if (new_len < dist[next_word_idx][temp_cons]) {
                    dist[next_word_idx][temp_cons] = new_len;
                    pq.push({-new_len, {next_word_idx, temp_cons}});
                }
            }
        }
    }

    // --- Paso 3: Respuesta Final ---
    int result = INF;
    if (n > 0) {
        // La respuesta es la longitud mínima encontrada para llegar a la última palabra,
        // sin importar con cuántas consonantes termine (0, 1 o 2).
        result = std::min({dist[n - 1][0], dist[n - 1][1], dist[n - 1][2]});
    }

    if (result == INF) {
        std::cout << "*" << std::endl; // Si no se encontró ninguna solución válida.
    } else {
        std::cout << result << std::endl;
    }
}

int main() {
    // Configuración para que la entrada/salida en C++ sea más rápida.
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    solve();
    
    return 0;
}