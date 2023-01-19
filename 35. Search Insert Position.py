class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:
        n=len(nums)//2
        nn=len(nums)
        if target>=nums[n]:
            if target==nums[n]: return n
            else: 
                while target>nums[n]:
                    n+=1
                    if n==nn:
                        return nn
                return n
        else:
            while target<=nums[n]:
                if target==nums[n]:
                    return n
                n=n-1
                if n==-1:
                    return 0
            return n+1

nums = [1, 3, 5, 7, 8, 10]
target=4
out=Solution().searchInsert(nums, target)
print(out)
