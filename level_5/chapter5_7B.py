"""
Efficienty of Implementation
* Tabulation is a Dynamic programming technique to store the computed results of subproblems to avoid redundant calculations.
    - The recursive implementation repeatedly invokes lis(hi) invokes on same hi
    - Considering how many times lis(10) is called on an initial list of size 20.
* For the approach to work:
    - Solve smallest subsprobles first and store results
    - Compose solution from previously computed subproblems.
"""
A = [3, 10, 2, 1, 20]  # Example list for testing

def lis(hi):

    longest = 1
    for j in range(hi):
        if A[j] < A[hi]:
            longest = max(longest, 1 + lis(j))
    return longest


print(lis(len(A) - 1))


# Using tabulation for longest increasing Subsequence
def lis_tabulation(A):
    N = len(A)
    LIS = [1] * N # Length of LIS ENDING  at A[i]
    for i in range(N):       # Solve problemas smallest to largest (i.e., from the beginning of the list)
        for j in range(i):   # Considering all earlier subproblems
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:   # update if longer
                LIS[i] = LIS[j] + 1
    return max(LIS)          # find longest one

print(lis_tabulation(A))

# Example 2
def lis_tabulation_two(A):
    N = len(A)
    LIS = [1] * N # Length of LIS ENDING  at A[i]
    prev=[-1] * N
    for i in range(N):       # Solve problemas smallest to largest (i.e., from the beginning of the list)
        for j in range(i):   # Considering all earlier subproblems
            if A[j] < A[i] and LIS[j] + 1 > LIS[i]:   # update if longer
                LIS[i] = LIS[j] + 1
                prev[i]=j    # Remember that 2nd to last element for A[i] is A[j]


    i=LIS.index(max(LIS))          # find longest one
    result=[]                # Stores sequence in List
    while i != -1:
        result.append(A[i])
        i = prev[i]
    return list(reversed(result))        # Reverse to produce actual LIS
