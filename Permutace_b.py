#Jsou dána dvě přirozená čísla n a k. Hodnota k je z rozmezí od 1 do n!. 
#Navrhněte efektivní algoritmus, který najde v pořadí k-tou permutaci množiny čísel {1, 2, 3, ..., n} v lexikografickém uspořádání.

def find_first_Index(k, n):
    if (n == 1):
        return 0, k
    n -= 1
    first_perm_index = 0
    n_factorial = n
 
    while (k >= n_factorial and n > 1):
        n_factorial = n_factorial * (n - 1)
        n -= 1
    first_perm_index = k // n_factorial
    k = k % n_factorial
    return first_perm_index, k

def find_K_Permutation(n, k):
    result = ""
    s = set()
    for i in range(1, n + 1):
        s.add(i)
    k = k - 1
    for i in range(n):
        tmp = list(s)
        index, k = find_first_Index(k, n - i)
        result += str(tmp[index])
        tmp.pop(index)
        s = set(tmp)
    return result

n, k = map(int, input().split())
res = find_K_Permutation(n, k)
print(res)



