import numpy as np
m=4
n=5
n1 = np.array([1,2])
n2 = np.array([2])
n3 = np.array([3])
n4 = np.array([4])
n5 = np.array([3,4])

data = np.array([n1,n2,n3,n4,n5],dtype=object)
print(data)

with open('example.npz', 'wb') as f0:
    np.savez(f0,m=m,data=data)