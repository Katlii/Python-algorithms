#Jsou dána dvě kladná celá čísla k a n. Nalezněte a vypište všechna k-ciferná čísla s ciferným součtem rovným n. Čísla vypište v rostoucím pořadí.
#Příklad 1: Pro vstupní hodnoty k = 3, n = 5 jsou správným výsledkem úlohy tato čísla:
#104 113 122 131 140 203 212 221 230 302 311 320 401 410 500
#Navrhněte postup, který vyřeší úlohu nejen správně, ale také co nejrychleji (nebude dělat žádnou zbytečnou práci). 


from itertools import permutations as prm

def funkce(a, result, n, p, k):
    if n:
        for i in range(n, 0, -1):
            if i <= p:
                funkce(a + [i], result, n-i, i, k)
    else:
        if len(a) <= k:
            a += [0]*(k - len(a))
            for j in set(prm(a)):
                if j[0] != 0:
                    result.append(''.join(map(str,j)))
    return result
 
k, n = map(int, input().split())
arr = funkce([], [], n, 9, k)
print(*sorted(arr))



