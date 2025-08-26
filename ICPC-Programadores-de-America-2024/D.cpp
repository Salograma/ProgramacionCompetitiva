#include <iostream> // Para entrada/salida (cin, cout)
#include <cmath>    // Para la función sqrt y round

// ====================================================================================
// PROCESO DE PENSAMIENTO Y ESTRATEGIA
// ====================================================================================
// 1. El jugador 1 (inicial) pierde si el GCD de sus números elegidos es 1.
// 2. El divisor '1' es la "píldora venenosa" que fuerza al GCD a ser 1.
// 3. Jugando de forma óptima, ambos jugadores evitarán tomar el '1' hasta el final.
//    Por lo tanto, el '1' será el último divisor en ser elegido.
// 4. El problema se reduce a: ¿Quién toma el último divisor?
// 5. Esto depende de la paridad del número total de turnos, que es el número
//    de divisores de N (tau(N)).
//    - Si tau(N) es impar, el jugador 1 (turnos 1, 3, ...) toma el último turno y pierde.
//    - Si tau(N) es par, el jugador 2 (turnos 2, 4, ...) toma el último turno, y el jugador 1 gana.
// 6. El número de divisores, tau(N), es impar si y solo si N es un CUADRADO PERFECTO.
// 7. La solución final es simplemente verificar si N es un cuadrado perfecto.
// ====================================================================================

void solve() {
    // Usamos 'long long' porque N puede ser hasta 10^12.
    long long n;
    std::cin >> n;

    // --- Caso Especial ---
    // Si N es 1, el único divisor es {1}. El jugador 1 debe tomarlo y pierde.
    if (n == 1) {
        std::cout << "N" << std::endl;
        return;
    }

    // --- Lógica Principal: Verificar si N es un cuadrado perfecto ---
    
    // 1. Calculamos la raíz cuadrada. sqrt() devuelve un tipo de punto flotante (double o long double).
    //    Es importante usar un tipo de alta precisión para minimizar errores.
    long double root = sqrt((long double)n);
    
    // 2. Redondeamos al entero más cercano. Esto es más robusto que un simple casteo (truncamiento).
    long long s = round(root);

    // 3. Verificamos si el cuadrado del entero es exactamente igual a N.
    //    Esta es la prueba definitiva y evita problemas de precisión.
    if (s * s == n) {
        // N es un cuadrado perfecto -> número impar de divisores -> P1 pierde.
        std::cout << "N" << std::endl;
    } else {
        // N no es un cuadrado perfecto -> número par de divisores -> P1 gana.
        std::cout << "Y" << std::endl;
    }
}

int main() {
    // Configuración para que la entrada/salida en C++ sea más rápida.
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    solve();
    
    return 0;
}