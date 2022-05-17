def nextPermutation(self, permutace):
        n=len(permutace)
        if n<2:
            return permutace
        inverse=-1
        i=n-2
        while i>=0:
            if permutace[i]<permutace[i+1]:
                inverse=i
                break
            i-=1
        if inverse<0:
            permutace.sort()
            i=0
            while permutace[i]==0:
                i+=1
            if i !=0:
                permutace[0], permutace[i]=permutace[i], permutace[0]
            return permutace
        i=n-1
        while i>=0:
            if permutace[inverse]<permutace[i]:
                permutace[inverse], permutace[i]=permutace[i],permutace[inverse]
                break
            i-=1
        permutace[inverse+1:]=reversed(permutace[inverse+1:])
        return permutace

n=int(input())
k=input().split()
res= nextPermutation(n, k)
print(' '.join(str(x) for x in res))
            
            
   
