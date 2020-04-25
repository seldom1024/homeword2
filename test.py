
t = []
s = input()
for i in s:
    if i not in t:
        t.append(i)
c = 0
for i in t:
    c = c+eval(i)
print(c)