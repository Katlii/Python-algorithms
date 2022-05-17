k, n = map(int, input().split())
 
i = 1*(10**(k-1))
e = n*(10**(k-1))
while i <= e:
    summ = y = 0
    a = i
    while y < k:
        summ += a%10
        a //= 10
        y+=1
    if summ == n:
        print(i)
    i+=1



