#include <iostream>
#include <vector>
#include <iomanip>
#include <algorithm>
#include <cmath>

// Usamos 'long double' para la máxima precisión posible.
using LD = long double;

struct Meteor {
    LD X, Y, Vx, Vy;
};

// Función que calcula el área en un tiempo t.
LD calculate_area(LD t, int n, const std::vector<Meteor>& meteors) {
    LD min_x = 1e18, max_x = -1e18;
    LD min_y = 1e18, max_y = -1e18;

    for (int i = 0; i < n; ++i) {
        LD px = meteors[i].X + t * meteors[i].Vx;
        LD py = meteors[i].Y + t * meteors[i].Vy;
        min_x = std::min(min_x, px);
        max_x = std::max(max_x, px);
        min_y = std::min(min_y, py);
        max_y = std::max(max_y, py);
    }
    return (max_x - min_x) * (max_y - min_y);
}

void solve() {
    int n;
    std::cin >> n;
    std::vector<Meteor> meteors(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> meteors[i].X >> meteors[i].Y >> meteors[i].Vx >> meteors[i].Vy;
    }

    // Búsqueda Ternaria directamente sobre la función de Área.
    LD low = 0.0;
    LD high = 4e9; // Límite superior muy seguro para t.

    // 200 iteraciones son más que suficientes para la precisión de long double.
    for (int i = 0; i < 200; ++i) {
        LD m1 = low + (high - low) / 3.0;
        LD m2 = high - (high - low) / 3.0;
        if (calculate_area(m1, n, meteors) < calculate_area(m2, n, meteors)) {
            high = m2;
        } else {
            low = m1;
        }
    }

    LD min_area = calculate_area(low, n, meteors);
    
    // Comprobar explícitamente t=0 sigue siendo una buena práctica.
    LD area_at_zero = calculate_area(0.0, n, meteors);

    // Imprimir el resultado con la precisión requerida.
    std::cout << std::fixed << std::setprecision(15) << std::min(min_area, area_at_zero) << std::endl;
}

int main() {
    // Configuración de Fast I/O para C++.
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
    solve();
    return 0;
}