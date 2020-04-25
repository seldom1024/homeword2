from functools import reduce
l1 = [{1, 2, 3}, {3}, {2, 3}]
# 交集
l2 = reduce(lambda x, y: x & y, l1)
# 并集
l3 = reduce(lambda x, y: x | y, l1)
