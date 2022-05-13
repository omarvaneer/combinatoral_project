import numpy as np
m=4
n=5
#start counting from 0
n1 = np.array([1,2],dtype=int)
n2 = np.array([2],dtype=int)
n3 = np.array([3],dtype=int)
n4 = np.array([0],dtype=int)
n5 = np.array([3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5],dtype=object)
print(data)

with open('example.npz', 'wb') as f0:
    np.savez(f0,m=m,data=data)