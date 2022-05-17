import numpy as np
import pandas as pd
import os

#ill just load everything into a dataframe and send it to csv

data = pd.DataFrame(columns=['name','k','time','result'])
output_folder = "exhaustive_output"

counter = 0
for filename in os.listdir(output_folder):
    header = filename.split('.')[0]
    metadata = header.split('_')
    file = open(os.path.join(output_folder,filename), "r")
    val = int(file.readline())

    data.loc[counter] = [metadata[0],metadata[1][1:],metadata[2][1:],val]
    counter +=1

data.to_csv("results.csv",index=False)
