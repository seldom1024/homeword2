li = ['taibai ', 'alexC', 'Abc ', 'egon', 'Ritian', 'Wusir', '  aqC']


# (1)查找列表li中的元素，移除每个元素的空格
def change(lis):
    for index, item in enumerate(lis):
        lis[index] = item.lstrip()


# (2)找出以‘R’或者‘a’开头，并以‘C’结尾的所有元素
def lookup(lis):
    lis2 = []
    for item in lis:
        if (item[0] == 'R' or item[0] == 'a' ) and item[len(item)-1] == 'C':
            lis2.append(item)
    return lis2


change(li)
print(li)
lis3 = lookup(li)
print(lis3)
