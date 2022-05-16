import numpy as np

dataset = np.load('benchmark/scp41.npz',allow_pickle=True)
#dataset = np.load('example.npz',allow_pickle=True)
m = dataset['m']
data = dataset['data']

for r in range(data.size):
    print(data[r])