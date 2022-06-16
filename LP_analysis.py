import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
import os

lpdata = pd.read_csv(os.path.join("AMPL_export","LP_out_results.csv"))
lpdata.columns = ['name', 'lp_result', 'lp_mink', 'm','n']
lpdata = lpdata[['name','m','n','lp_result', 'lp_mink']]

grdata = pd.read_csv("greedy_output_results.csv")
grdata.columns = ['name','gr_time','gr_result', 'gr_mink', 'm','n']
grdata = grdata[['name','m','n','gr_time','gr_result', 'gr_mink']]
data = reduce(lambda  left,right: pd.merge(left,right,on=['name','m','n'],
                                            how='outer'), [lpdata,grdata])

#filter out the problems too big for lp solver
data1 = data[data["lp_result"]==1]

#evaluate gaps between greedy result and lp lower bound
data1.insert(loc=len(data1.columns), column='gap', value=data1["gr_mink"]-data1["lp_mink"])
data1.insert(loc=len(data1.columns), column='gap_percent', value=100*data1["gap"]/data1["lp_mink"])

#helper functions organized horribly
def name2group(name):
    switch={
      'h':1,
      'r':2,
      's':3,
      }
    return switch.get(name[0],-1)

def names2groups(names):
    group = []
    for name in names:
        group.append(name2group(name))
    return group

data1.insert(loc=len(data1.columns), column='group', value=names2groups(data1["name"]))

#visualize
fig,ax = plt.subplots()
l1=ax.scatter(data1["n"],data1["gap"],c=data1["group"])
ax.set_title("Gap Between Greedy result and LP bound")
ax.set_xlabel("Number of Subsets")
ax.set_ylabel("Gap")

fig2,ax2 = plt.subplots()
l2=ax2.scatter(data1["n"],data1["gap_percent"],c=data1["group"])
ax2.set_title("Gap % Between Greedy result and LP bound")
ax2.set_xlabel("Number of Subsets")
ax2.set_ylabel("Gap (% of LP bound)")

plt.show()
print(data1)
data1.to_csv("temp_results.csv",index=False)
#breakdown by type:
#all handmade and some random were small enough
#only one group of the benchmarks from literature was solvable by cplex demo license
#the random section is actually 2 random sections. The randomly generated instances were generated in 3 size clusters.
#Two of the clusters can be seen but the third was too big and got clipped