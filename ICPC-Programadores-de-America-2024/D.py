import sys

def solve():
    # ====================================================================================
    # PROCESO DE PENSAMIENTO FINAL
    # ====================================================================================
    # 1. El jugador 1 (P1) gana si el GCD de los números que elige es > 1.
    # 2. Para lograr esto, P1 solo necesita asegurarse de que al menos uno de los
    #    números que elija sea mayor que 1.
    # 3. En su primer turno, ¿puede P1 siempre elegir un divisor mayor que 1?
    # 4. SÍ, puede hacerlo, siempre y cuando N > 1. Si N > 1, el propio N es un
    #    divisor mayor que 1. P1 puede simplemente tomar N.
    # 5. Después de que P1 toma N, su GCD actual es N (> 1). En sus turnos futuros,
    #    mientras queden divisores > 1, P1 puede seguir eligiéndolos para mantener
    #    su GCD > 1. P2 nunca puede forzar a P1 a tomar solo el 1, porque P1
    #    siempre puede elegir otro divisor si existe.
    # 6. La única situación en la que P1 no puede hacer esto es si no hay ningún
    #    divisor > 1 para empezar. Esto ocurre si y solo si N = 1.
    # 7. Por lo tanto, P1 gana siempre, excepto cuando N=1.
    # ====================================================================================
    
    try:
        n_str = sys.stdin.readline()
        if not n_str: return
        N = int(n_str)
    except (IOError, ValueError):
        return

    if N == 1:
        print("N")
    else:
        print("Y")

solve()