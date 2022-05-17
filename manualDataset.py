import numpy as np
import os

#4 datasets created by hand

#set 1
m=4
n=5
k1=int(n/3)
k2=int(2*n/3)
#start counting from 0
n1 = np.array([1,2],dtype=int)
n2 = np.array([2],dtype=int)
n3 = np.array([3],dtype=int)
n4 = np.array([0],dtype=int)
n5 = np.array([3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5],dtype=object)
#print(data)

with open(os.path.join('benchmark','h1_k')+str(k1)+'.npz', 'wb') as f0:
    np.savez(f0,m=m,k=k1,data=data)
with open(os.path.join('benchmark','h1_k')+str(k2)+'.npz', 'wb') as f1:
    np.savez(f1,m=m,k=k2,data=data)

#set 2
m=5
n=5
k1=int(n/3)
k2=int(2*n/3)
#start counting from 0
n1 = np.array([0,2],dtype=int)
n2 = np.array([0,3],dtype=int)
n3 = np.array([4],dtype=int)
n4 = np.array([2],dtype=int)
n5 = np.array([4,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5],dtype=object)
#print(data)

with open(os.path.join('benchmark','h2_k')+str(k1)+'.npz', 'wb') as f2:
    np.savez(f2,m=m,k=k1,data=data)
with open(os.path.join('benchmark','h2_k')+str(k2)+'.npz', 'wb') as f3:
    np.savez(f3,m=m,k=k2,data=data)

#set 3
m=5
n=6
k1=int(n/3)
k2=int(2*n/3)
#start counting from 0
n1 = np.array([0,2],dtype=int)
n2 = np.array([4,3],dtype=int)
n3 = np.array([3],dtype=int)
n4 = np.array([2],dtype=int)
n5 = np.array([1,0],dtype=int)
n6 = np.array([1,3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5,n6],dtype=object)
#print(data)

with open(os.path.join('benchmark','h3_k')+str(k1)+'.npz', 'wb') as f4:
    np.savez(f4,m=m,k=k1,data=data)
with open(os.path.join('benchmark','h3_k')+str(k2)+'.npz', 'wb') as f5:
    np.savez(f5,m=m,k=k2,data=data)

#set 4
m=6
n=6
k1=int(n/3)
k2=int(2*n/3)
#start counting from 0
n1 = np.array([0,2,5],dtype=int)
n2 = np.array([4,3],dtype=int)
n3 = np.array([3,5],dtype=int)
n4 = np.array([2,4,1],dtype=int)
n5 = np.array([1,0],dtype=int)
n6 = np.array([3,0],dtype=int)

data = np.array([n1,n2,n3,n4,n5,n6],dtype=object)
#print(data)

with open(os.path.join('benchmark','h4_k')+str(k1)+'.npz', 'wb') as f6:
    np.savez(f6,m=m,k=k1,data=data)
with open(os.path.join('benchmark','h4_k')+str(k2)+'.npz', 'wb') as f7:
    np.savez(f7,m=m,k=k2,data=data)