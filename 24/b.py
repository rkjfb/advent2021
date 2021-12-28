a = "abcdefghijklmnopqrstuvwxyz"
print(len(a))

b =[6,14,14,10,9,12,8,13,12,6,9,15,4,10]

r1 = ""
r2 = ""
r3 = ""
r4 = ""
r5 = ""
r6 = ""
for i in b:
    r1 += a[i]
    r2 += a[i+1]
    r3 += a[i-1]
    r4 += a[26-i]
    r5 += a[25-i]
    r6 += a[27-i]

print(r1)
print(r2)
print(r3)
print(r4)
print(r5)
print(r6)
