
def generateParenthesis(n):
    parentesis = [[] for _ in range(n)]
    parentesis[0] = ["()"]
    if n == 1:
        print(parentesis[0])
        return parentesis[0]
    else:
        for i in range(1,n):
            for j in parentesis[i-1]:
                parentesis[i].append(f"({j})")
                parentesis[i].append(f"{j}()")
    print(parentesis)

n = int(input("Ingrese un numero "))
generateParenthesis(n)