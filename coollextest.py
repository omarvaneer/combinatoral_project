import numpy as np

#cool-lex algorithm for exhaustively generating combinations
#https://www.sciencedirect.com/science/article/pii/S0012365X07009570


n=6
k=4

t=k
s=n-k

initial = np.zeros([n])
for i in range(k):
    initial[i] = True

print(initial)
b = initial

x = t
y = t
while(x<s+t):
    b[int(x-1)] = False
    b[int(y-1)] = True
    b[0] = b[int(x)]
    b[int(x)] = 1
    x = x+1-(x-1)*b[1]*(1-b[0])
    y=b[0]*y+1
    print(b)