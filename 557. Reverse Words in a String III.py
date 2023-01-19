class Solution:
    def reverseWords(self, s: str) -> str:
        s=s.split()
        A=''
        for a in range(len(s)):
            s[a]=list(s[a])
        for a in s:
            a.reverse()
        for i in range (len(s)):
            A=A+''.join(s[i])
            if i!=len(s)-1:
                A=A+' '
            
        return A
            



s = "Let's take LeetCode contest"
out=Solution().reverseWords(s)
print(out)
