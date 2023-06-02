from itertools import combinations as comb
from itertools import permutations as perm


def main():
  num_partitions = 6

  pairs = list(comb(range(num_partitions), 2))
  print(pairs)
  print()

  i = 0
  while i + 1 < len(pairs):
    if pairs[i + 1][0] in pairs[i] or pairs[i + 1][1] in pairs[i]:
      i += 1
    else:
      pairs = pairs[:i + 1] + pairs[i + 2:] + [pairs[i + 1]]

  print(pairs)


  # pairs = list(perm(range(num_partitions), 2))
  # print(pairs)
  # print()

  # repo = set()

  # i = 0
  # result_len = len(pairs) // 2
  # while i + 1 < result_len:
  #   if pairs[i] in repo:
  #     pairs = pairs[:i] + pairs[i + 1:]
  #   elif pairs[i + 1][0] == pairs[i][1]:
  #     print(pairs[i])
  #     repo.add((pairs[i][1], pairs[i][0]))
  #     i += 1
  #   else:
  #     pairs = pairs[:i + 1] + pairs[i + 2:] + [pairs[i + 1]]

  # print(result_len, pairs[:result_len])
  # print(len(list(comb(range(num_partitions), 2))))



if __name__ == '__main__':
  main()
