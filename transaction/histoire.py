import random

r=[]
l= ["c1", "c2", "r1(x)", "w1(y)", "r2(x)", "w2(z)", "r3(y)", "w3(x)"]
for i in range(20):
    r.append(random.choice(l))


print(l)
key = []
for i in range(3):
   key.append(str("T_"+str(i)))

print(key)