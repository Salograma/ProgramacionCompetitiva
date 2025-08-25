#ProblemaMonedas
import math
def Monedas(valor, monedas):
    dp = [math.inf] * (valor+1)
    dp[0] = 0
    dp[1] = 1 if 1 in monedas else math.inf
    for i in range(2,valor+1):
        for j in monedas:
            dp[i] = min(dp[i], dp[i-j] + 1)
    print(dp[valor+1])

Monedas(10,[4,2])
