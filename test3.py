lis = [2, 3, 'k', ['qwe', 20, ['k', ['tt', 3, '1']], 89], 'tt', 'adv']


# 定义递归函数
def lookup(tem):
    for index, item in enumerate(tem):
        # 如果是list类型继续寻找
        if isinstance(item, list):
            lookup(tem[index])
        else:
            # 判断是否是字符串
            if isinstance(item, str):
                if tem[index] == '1':
                    tem[index] = 101


lookup(lis)
print(lis)

# 第二种方法直接修改但是不可取
