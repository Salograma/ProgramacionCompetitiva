import math
class Solution(object):
    def coinChange(self, coins, amount):
        if amount == 0:
            return 0
        dp = [float("inf")] * (amount+1)
        dp[0] = 0
        dp[1] = 1 if 1 in coins else float("inf")
        for i in range(2,amount+1):
            for j in coins:
                if i >= j:
                    dp[i] = min(dp[i], dp[i-j] + 1)
        if dp[amount] == float("inf"):
            return -1
        else:
            return dp[amount]