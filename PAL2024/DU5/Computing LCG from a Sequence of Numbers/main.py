#!/usr/bin/env python3

import math
from itertools import combinations

def extended_gcd(a, b):
    # Returns (g, x, y) such that a*x + b*y = g = gcd(a,b).
    if b == 0:
        return (a, 1, 0)
    else:
        g2, x2, y2 = extended_gcd(b, a % b)
        return (g2, y2, x2 - (a // b) * y2)

def mod_inverse(a, m):
    # Computes inverse of a mod m, assuming gcd(a,m)=1.
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None
    return x % m

def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return n == 2 or n == 3
    r = int(math.isqrt(n))
    f = 5
    while f <= r:
        if n % f == 0 or n % (f+2) == 0:
            return False
        f += 6
    return True

def factor_within_range(G, pmin, pmax):
    """
    Factor out all primes within [pmin..pmax] that divide G.
    Return a dictionary: prime -> 1 if prime divides G (≥1 times).
    We only need exponent=1 because each prime in M=(p1*p2*...pF)^2 is distinct.
    """
    factors = {}
    
    # We'll do a standard prime sieve or direct checking up to pmax (since pmax ≤ 503 is not huge).
    # For bigger pmax, one might do something more optimized, but for <= 503 this is fine.
    prime_list = [p for p in range(pmin, pmax+1) if is_prime(p)]
    
    for p in prime_list:
        if p > G:
            break
        # Check if p divides G
        if G % p == 0:
            factors[p] = 1  # we only store it as a potential factor
            # We'll divide out p completely from G to speed up subsequent checks
            while G % p == 0:
                G //= p
    
    # It's possible G is now bigger than 1 but not in [pmin..pmax].
    # If G>1 at this point and is prime but outside [pmin..pmax], it can't be part of M (by problem statement).
    return list(factors.keys())

def gcd_of_list(lst):
    g = 0
    for val in lst:
        g = math.gcd(g, abs(val))
    return g

def check_full_period(A, C, M):
    """
    Hull–Dobell: 
      1) gcd(C,M)=1
      2) every prime factor of M divides (A-1)
      3) if 4|M then 4|(A-1)
    """
    if math.gcd(C, M) != 1:
        return False
    
    # Factor M to find distinct primes
    # (We know M is a perfect square of distinct primes ≥5, but let's do generic factor)
    remainder = M
    prime_factors = set()
    d = 2
    while d*d <= remainder:
        if remainder % d == 0:
            prime_factors.add(d)
            while remainder % d == 0:
                remainder //= d
        d += 1 if d==2 else 2
    if remainder > 1:
        prime_factors.add(remainder)
    
    for pf in prime_factors:
        if (A - 1) % pf != 0:
            return False
    if M % 4 == 0:
        if (A - 1) % 4 != 0:
            return False
    
    return True

def solve_lcg(Pmax, Mmax, N, seq):
    # 1) Compute differences d_i = x_{i+1}-x_i (ordinary integer difference).
    diffs = [seq[i+1] - seq[i] for i in range(N-1)]

    # 2) Compute Delta_n = d_n*d_{n+2} - d_{n+1}^2, for n=0..(N-3)-1 => n up to N-3
    #    Actually, since d_i is 0-based in the array, we do for n in [0..N-3]
    #    We need up to d_{n+2}, so n goes up to N-3-1 => N-3-1 = N-4
    #    But simpler is: for n in range(N-2): we only use n up to N-3 actually.
    #    We'll do a safe approach:
    Deltas = []
    for n in range(N-2):
        # we want d_n*d_{n+2} - d_{n+1}^2, but watch array bounds
        if n+2 < len(diffs):
            val = diffs[n]*diffs[n+2] - diffs[n+1]*diffs[n+1]
            Deltas.append(val)
    if not Deltas:
        # If N=3 or 4, we might have fewer deltas, but problem states N>=10
        pass

    # 3) gcd all these Deltas to get G
    G = gcd_of_list(Deltas)
    if G == 0:
        # This might happen if all Deltas are 0 => means the sequence is linear?
        # But for a typical "full period" LCG with large M, that is extremely unlikely. 
        # We'll handle it anyway:
        # fallback to an approach if all deltas are zero => we might guess M is big 
        # or there's a special pattern. We'll just set G=0 => no prime factor from gcd. 
        # That means we can't do much. Could fallback. But let's just proceed.
        G = 0

    # 4) Factor out primes in [5..Pmax] from G
    prime_candidates = factor_within_range(abs(G), 5, Pmax)
    
    # prime_candidates is the list of distinct primes in [5..Pmax] that divide G at least once.
    # M is formed by *some subset* of these prime_candidates, each used exactly once in the product, 
    # and then squared. So let's build subsets from prime_candidates.

    # We'll keep only subsets whose squared product is <= Mmax and > max(seq).
    Xmax = max(seq)
    
    # A function to check the entire sequence quickly for a given (A,C,M)
    def check_sequence(A, C, M):
        for i in range(N-1):
            if (A*seq[i] + C) % M != seq[i+1]:
                return False
        return True
    
    # We'll do standard approach to solve for (A,C) from consecutive triple
    #   x_{k+1} = (A*x_k + C) mod M
    #   x_{k+2} = (A*x_{k+1} + C) mod M
    # => A = ((x_{k+2}-x_{k+1}) * inv(x_{k+1}-x_{k})) mod M, etc.
    def find_AC(M):
        # We can pick several consecutive triples, hoping gcd(x_{i+1}-x_i, M)=1 for some i.
        for i in range(N-2):
            x1, x2, x3 = seq[i], seq[i+1], seq[i+2]
            diff = (x2 - x1) % M
            if math.gcd(diff, M) == 1:
                invd = mod_inverse(diff, M)
                if invd is None: 
                    continue
                A = ((x3 - x2) % M)*invd % M
                C = (x2 - A*x1) % M
                return (A, C)
        return None

    # Now let's do subsets of prime_candidates:
    # For large prime_candidates, we could do a backtracking approach. 
    # But typically prime_candidates won't be huge because GCD-based approach is quite selective.
    solutions = []
    
    # We'll create all subsets of prime_candidates:
    # The number of subsets can still be up to 2^(#prime_candidates), but #prime_candidates
    # is typically small for big M in these puzzle contexts.
    # If it's big, we can do further pruning. 
    # We'll do a standard subset enumeration but watch product carefully.

    def backtrack(primes, start_index, current_prod):
        """
        Build subsets from 'primes[start_index..]' trying to pick or not pick each prime.
        current_prod is the product of chosen primes so far.
        """
        # We can check the squared product at each step.
        sq = current_prod * current_prod
        if sq > Xmax and sq <= Mmax:
            # It's a valid candidate M
            yield sq
        
        # If continuing might exceed Mmax, stop
        if sq > Mmax:
            return
        
        for i in range(start_index, len(primes)):
            p = primes[i]
            new_prod = current_prod * p
            if new_prod * new_prod > Mmax:
                # further picks only make product bigger
                break
            yield from backtrack(primes, i+1, new_prod)

    # Gather all candidate M from subsets:
    candidate_M = set()
    # We also consider the possibility that M might be just 1 prime or multiple:
    for mval in backtrack(sorted(prime_candidates), 0, 1):
        candidate_M.add(mval)
    
    # Sort them:
    candidate_M = sorted(candidate_M)

    # For each candidate M, solve for (A, C) and check the sequence + full-period:
    for M in candidate_M:
        # Solve for A, C:
        AC = find_AC(M)
        if AC is None:
            continue
        A, C = AC
        # Check entire sequence
        if check_sequence(A, C, M):
            # Check Hull-Dobell
            if check_full_period(A, C, M):
                return (A, C, M)
    
    # The puzzle states exactly one solution. 
    # If none found, we return None as fallback (but presumably won't happen).
    return None

def main():
    # Example of reading from standard input. 
    # For your environment, adapt as needed or read from a file.
    Pmax, Mmax, N = map(int, input().split())
    seq = list(map(int, input().split()))

    # Solve
    ans = solve_lcg(Pmax, Mmax, N, seq)
    if ans is not None:
        A, C, M = ans
        print(A, C, M)
    else:
        print("No solution found (unexpected).")

if __name__ == "__main__":
    main()
