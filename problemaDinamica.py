#GRID PROBLEM
def minPathSum(grid):
    ancho = len(grid)
    alto = len(grid[0])
    dp = [0] * ancho
    for i in range(ancho):
        dp[i] = [0] * alto
    dp[0][0] = grid[0][0]
    for i in range(ancho):
        for j in range(alto):
            dp[i][j] = max(dp[i-1][j]+grid[i][j],dp[i][j-1]+grid[i][j])
    return dp

grid = [[1,2],[3,4]]
minPathSum(grid)