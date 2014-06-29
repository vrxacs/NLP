# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 15:27:16 2014

@author: Valeri
"""

# FUTURE: For now the cost of substituting is fixed,
#       but in the future we might want a letter-specific cost
def subCost(source, target):
    if source == target:
        return 0
    else:
        return 2

# FUTURE: For now the cost of inserting is fixed,
#       but in the future we might want a letter-specific cost
def insCost(char):
    return 1

# FUTURE: For now the cost of deleting is fixed,
#       but in the future we might want a letter-specific cost
def delCost(char):
    return 1

def minEditDist(target, source):
    """
    This is an implementation of the minimum edit distance algorithm,
    presented in Chapter 3 of "Speech and Language Processing, 2nd ed"
    by Jurafsky D., Martin J.
    """
    n = len(target)
    m = len(source)
    dist = [None] * (n+1)

    for i in range(n+1):
        dist[i] = [None] * (m+1)
    
    # Initialize the 0th row and column to be the distance from the empty string
    dist[0][0] = 0
    for i in range(1, n+1):
        dist[i][0] = dist[i-1][0] + insCost(target[i-1])
    for j in range(1, m+1):
        dist[0][j] = dist[0][j-1] + delCost(source[j-1])

    for i in range(1, n+1):
        for j in range(1, m+1):
            dist[i][j] = min(dist[i-1][j] + insCost(target[i-2]), dist[i-1][j-1] + subCost(source[j-2], target[i-2]), dist[i][j-1] + delCost(source[j-2]))
    
    return dist[n][m]