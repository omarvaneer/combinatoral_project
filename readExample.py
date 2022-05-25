import numpy as np

dataset = np.load('benchmark/scp41_k333.npz',allow_pickle=True)
#dataset = np.load('example_k1.npz',allow_pickle=True)
m = dataset['m']
k=dataset['k']
data = dataset['data']

for r in range(data.size):
    print(data[r])