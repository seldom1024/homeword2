# li1 = input()
# li2 = input()
# # change to list
# liA = li1.split(" ")
# liB = li2.split(" ")
# # get the min
# le = len(liA) if liA < liB else len(liB)
# di = {}
# for i in range(le):
#     di[liA[i]] = liB[i]
# print(di)


def multiplicationTable():
    for i in range(1, 10):
        for j in range(1, i+1):
            print(j, end='')
            print("{}*{}={}".format(j, i, i*j), end=' ')
        print()

multiplicationTable()