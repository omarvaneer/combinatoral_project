import numpy as np
import pandas as pd
import os

#ill just load everything into a dataframe and send it to csv

data = pd.DataFrame(columns=['name','time','result','min k','m (true set)','n (number of subsets)'])
output_folder = "exhaustive_output"
npz_folder = "benchmark"

counter = 0
for filename in os.listdir(output_folder):
    header = filename.split('.')[0]
    metadata = header.split('_')
    file = open(os.path.join(output_folder,filename), "r")
    res = int(file.readline())
    minK = int(file.readline())

    dataset = np.load(os.path.join(npz_folder,metadata[0]+'.npz'),allow_pickle=True)
    m = dataset['m']#total unique elements of set
    n = dataset['data'].size#array of subsets

    data.loc[counter] = [metadata[0],metadata[1][1:],res,minK,m,n]
    counter +=1
    file.close()

data.to_csv(output_folder+"_results.csv",index=False)

"""
exhaustive search output file format:
    row1: exit code
        1: optimal minimum k found
        -1: no set cover for any k
        0: timeout reached
    row2: k value
        if row1 == 1, k is optimal
        if row1 == 0, k is the best k found before timeout
        0: something went wrong. this shouldn't happen
        -1: no set cover for any k - also shouldn't happen
"""

#insight: the 1 minute and 10 minute results are often the same. 
# certain k values can easily result in so many conbinations that both versions will get stuck there. 
# the 10 minute one gets a little farther but usually not enough to move on to a different k value. 