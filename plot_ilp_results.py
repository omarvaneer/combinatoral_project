import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
import os
import numpy as np


ilpdata = pd.read_csv(os.path.join("AMPL_export","ILP_out_results.csv"))
ilpdata.columns = ['name', 'ilp_result', 'ilp_mink', 'm','n']
ilpdata = ilpdata[['name','m','n','ilp_result', 'ilp_mink']]
ilpdata = ilpdata[ilpdata["ilp_result"]==1]
whatworked = list(ilpdata["name"])

fig,ax = plt.subplots()
l1=ax.scatter(ilpdata["n"],ilpdata["ilp_mink"])
ax.set_title("Minimum k vs Number of Subsets")
ax.set_xlabel("Number of Subsets")
ax.set_ylabel("Minimum k")

exhaustivedata = pd.read_csv("exhaustive_output_results.csv")
exhaustivedata.columns = ['name', 'time', 'exh_result', 'exh_mink', 'm','n']
exhaustivedata = exhaustivedata[exhaustivedata['time']==600]
exhaustivedata.drop(columns='time')
exhaustivedata = exhaustivedata[exhaustivedata.name.isin(whatworked)]

data = reduce(lambda  left,right: pd.merge(left,right,on=['name','m','n'],
                                            how='outer'), [ilpdata,exhaustivedata])

print(data)

colors = np.where(exhaustivedata["exh_result"]==1,'b','r')

fig1,ax1 = plt.subplots()
l2=ax1.scatter(ilpdata["n"],abs(data["exh_mink"]-data["ilp_mink"]), c = colors)
ax1.set_title("Gap Between ILP and Exhaustive Search")
ax1.set_xlabel("Number of Subsets")
ax1.set_ylabel("Gap")

plt.show()