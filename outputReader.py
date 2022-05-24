import numpy as np
import pandas as pd
import os

#ill just load everything into a dataframe and send it to csv

data = pd.DataFrame(columns=['name','time','result','min k'])
output_folder = "exhaustive_output"

counter = 0
for filename in os.listdir(output_folder):
    header = filename.split('.')[0]
    metadata = header.split('_')
    file = open(os.path.join(output_folder,filename), "r")
    res = int(file.readline())
    minK = int(file.readline())

    data.loc[counter] = [metadata[0],metadata[1][1:],res,minK]
    counter +=1
    file.close()

data.to_csv("results.csv",index=False)

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