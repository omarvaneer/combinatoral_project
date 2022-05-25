import numpy as np
import os

#5 datasets created by hand

#set 1
m=4
n=5
#start counting from 0
n1 = np.array([1,2],dtype=int)
n2 = np.array([2],dtype=int)
n3 = np.array([3],dtype=int)
n4 = np.array([0],dtype=int)
n5 = np.array([3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5],dtype=object)
#print(data)

with open(os.path.join('benchmark','h1.npz'), 'wb') as f0:
    np.savez(f0,m=m,data=data)

#set 2
m=5
n=5
#start counting from 0
n1 = np.array([0,1,2],dtype=int)
n2 = np.array([0,1,3],dtype=int)
n3 = np.array([4],dtype=int)
n4 = np.array([2],dtype=int)
n5 = np.array([4,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5],dtype=object)
#print(data)

with open(os.path.join('benchmark','h2.npz'), 'wb') as f1:
    np.savez(f1,m=m,data=data)

#set 3
m=5
n=6
#start counting from 0
n1 = np.array([0,2],dtype=int)
n2 = np.array([4,3],dtype=int)
n3 = np.array([3],dtype=int)
n4 = np.array([2],dtype=int)
n5 = np.array([1,0],dtype=int)
n6 = np.array([1,3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5,n6],dtype=object)
#print(data)

with open(os.path.join('benchmark','h3.npz'), 'wb') as f2:
    np.savez(f2,m=m,data=data)

#set 4
m=6
n=6
#start counting from 0
n1 = np.array([0,2,5],dtype=int)
n2 = np.array([4],dtype=int)
n3 = np.array([3,5],dtype=int)
n4 = np.array([2,1],dtype=int)
n5 = np.array([1,0],dtype=int)
n6 = np.array([3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5,n6],dtype=object)
#print(data)

with open(os.path.join('benchmark','h4.npz'), 'wb') as f3:
    np.savez(f3,m=m,data=data)

#set 5
m=9
n=8
#start counting from 0
n1 = np.array([0,2,5],dtype=int)
n2 = np.array([4,3],dtype=int)
n3 = np.array([3,5],dtype=int)
n4 = np.array([2,4,1],dtype=int)
n5 = np.array([1,0,6],dtype=int)
n6 = np.array([3,0,7],dtype=int)
n7 = np.array([7],dtype=int)
n8 = np.array([8],dtype=int)

data = np.array([n1,n2,n3,n4,n5,n6,n7,n8],dtype=object)
#print(data)

with open(os.path.join('benchmark','h5.npz'), 'wb') as f4:
    np.savez(f4,m=m,data=data)