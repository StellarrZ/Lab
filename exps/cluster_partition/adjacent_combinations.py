from itertools import combinations as comb
from itertools import permutations as perm
from collections import deque, Counter, defaultdict
import heapq


def verifier(fn):
  def decorated_fn():
    res = fn()
    l = list(map(lambda x: tuple(sorted(x)), res)) + list(comb(range(num_partitions), 2))
    # print(Counter(l))
    assert (max(Counter(l).values()) == min(Counter(l).values()) == 2), "FAIL"
    print("PASS")
    return res
  
  return decorated_fn


# @verifier
# def heuristic():
#   res = []
#   credit = [set([j for j in range(num_partitions - 1, -1, -1) if j != i]) for i in range(num_partitions)]
#   cur = 0
#   while len(res) < num_partitions * (num_partitions - 1) / 2:
#     opt_idx, max_val = -1, float("-inf")
#     for j in credit[cur]:
#       if len(credit[j]) > max_val:
#         opt_idx, max_val = j, len(credit[j])
#     res.append((cur, opt_idx))
#     try:
#       credit[cur].remove(opt_idx)
#       credit[opt_idx].remove(cur)
#     except:
#       print("=== except === ", res)
#       return res
#     cur = opt_idx
  
#   return res


@verifier
def euler_path_traverse():
  res = []
  # adj-lists
  graph = [set([j for j in range(num_partitions) if j != i]) for i in range(num_partitions)]
  pre = 0
  # dfs
  stack = list(graph[0])
  while len(res) < num_partitions * (num_partitions - 1) / 2:
    cur = stack.pop()
    res.append((pre, cur))
    graph[pre].remove(cur)
    graph[cur].remove(pre)
    stack += graph[cur]
    pre = cur

  return res


""" 
  To contain Euler path
  must has odd number of vertices
  so that there is no vertex has odd degree
"""
if __name__ == '__main__':

  for num_partitions in range(3, 100, 2):
    print("\nnum_partitions = %d" % num_partitions)
    res = euler_path_traverse()
    # print(res, len(res))
