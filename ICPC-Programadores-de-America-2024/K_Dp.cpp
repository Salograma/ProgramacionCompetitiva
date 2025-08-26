#include <iostream>   // Para entrada/salida (cin, cout)
#include <vector>     // Para usar std::vector (arreglos dinámicos)
#include <string>     // Para usar std::string
#include <algorithm>  // Para usar std::min

// Se define una constante para representar un valor "infinito".
// Útil para inicializar distancias y encontrar mínimos.
const int INF = 1e9;

// Función auxiliar para determinar si un carácter es una vocal.
// Se incluye 'Y' como se especifica en el enunciado del problema.
bool is_vowel(char c) {
    return c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U' || c == 'Y';
}

void solve() {
    // ====================================================================================
    // PROCESO DE PENSAMIENTO Y ESTRATEGIA
    // ====================================================================================
    // PASO 0: DIAGNÓSTICO
    // El problema pide la "longitud mínima" de una construcción hecha paso a paso (palabra por palabra).
    // La decisión para la palabra `i` depende del resultado de la `i-1`. Esto es un claro
    // indicio para usar Programación Dinámica (DP).
    //
    // PASO 1: DEFINICIÓN DEL ESTADO
    // Para decidir si podemos añadir un prefijo, lo único que necesitamos saber del
    // acrónimo anterior es con cuántas consonantes consecutivas termina.
    // Estado: dp[i][j] = longitud mínima del acrónimo usando las primeras `i` palabras,
    // terminando con `j` consonantes (j = 0, 1, o 2).
    //
    // PASO 2: TRANSICIÓN Y OPTIMIZACIÓN DE ESPACIO
    // Para calcular los estados de la palabra `i`, solo necesitamos los resultados de la `i-1`.
    // Por lo tanto, no necesitamos una matriz N x 3. Optimizamos el espacio usando solo dos
    // vectores: `dp_prev` (para la palabra i-1) y `dp_curr` (para la palabra i).
    // La transición se hace probando cada prefijo de la palabra `i` desde cada estado válido
    // de la palabra `i-1`, simulando la concatenación y verificando la regla de las consonantes.
    //
    // PASO 3: ELECCIÓN DE LENGUAJE
    // Dado que el número de operaciones puede ser grande y el límite de tiempo es estricto,
    // C++ es la elección más segura para garantizar que la solución pase el TLE.
    // ====================================================================================

    // --- Lectura de la entrada ---
    int n;
    std::cin >> n;
    std::vector<std::string> words(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> words[i];
    }

    // --- Inicialización de la DP ---
    // dp_prev[j] almacenará la longitud mínima del acrónimo hasta la palabra anterior,
    // terminando con 'j' consonantes.
    std::vector<int> dp_prev(3, INF);

    // --- Paso 1: Casos Base (procesar la primera palabra, i=0) ---
    // Se calculan los estados iniciales posibles.
    for (int len = 1; len <= std::min((int)words[0].length(), 3); ++len) {
        std::string prefix = words[0].substr(0, len);
        
        int consonants = 0;
        bool valid = true;
        // Se verifica que el prefijo en sí mismo sea "pronunciable".
        for (char c : prefix) {
            if (!is_vowel(c)) {
                consonants++;
            } else {
                consonants = 0; // Las vocales reinician el contador.
            }
            if (consonants > 2) {
                valid = false;
                break;
            }
        }
        
        if (valid) {
            // Si el prefijo es válido, actualizamos el estado base.
            // La longitud es 'len' y termina con 'consonants' consonantes.
            dp_prev[consonants] = std::min(dp_prev[consonants], len);
        }
    }

    // --- Paso 2: Llenar la tabla de DP iterativamente (desde la segunda palabra) ---
    for (int i = 1; i < n; ++i) {
        // Vector para los resultados de la palabra actual 'i'.
        std::vector<int> dp_curr(3, INF);

        // Iteramos sobre cada estado final posible de la palabra anterior (i-1).
        for (int prev_j = 0; prev_j < 3; ++prev_j) {
            if (dp_prev[prev_j] == INF) { // Si el estado anterior es inalcanzable, lo saltamos.
                continue;
            }
            
            // Probamos añadir cada prefijo válido (longitud 1, 2 o 3) de la palabra actual.
            for (int len = 1; len <= std::min((int)words[i].length(), 3); ++len) {
                std::string prefix = words[i].substr(0, len);
                
                // Se simula la concatenación para verificar la validez de la transición.
                int temp_cons = prev_j; // Empezamos con las consonantes del estado anterior.
                bool valid_transition = true;
                for (char c : prefix) {
                    if (!is_vowel(c)) {
                        temp_cons++;
                    } else {
                        temp_cons = 0;
                    }
                    if (temp_cons > 2) { // Si se rompe la regla, la transición es inválida.
                        valid_transition = false;
                        break;
                    }
                }
                
                // Si la transición fue válida, actualizamos el estado correspondiente en la fila actual.
                if (valid_transition) {
                    // La nueva longitud es la anterior + la longitud del prefijo actual.
                    dp_curr[temp_cons] = std::min(dp_curr[temp_cons], dp_prev[prev_j] + len);
                }
            }
        }
        // La fila actual se convierte en la "previa" para la siguiente iteración.
        dp_prev = dp_curr;
    }

    // --- Paso 3: Respuesta Final ---
    int result = INF;
    if (n > 0) {
        // La respuesta es la longitud mínima encontrada para la última palabra,
        // sin importar con cuántas consonantes termine (0, 1 o 2).
        result = std::min({dp_prev[0], dp_prev[1], dp_prev[2]});
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