#convert instances to AMPL dat files

#if the dat files get too big, it might be easier to make a set of subsets as the constants in dat and 
#have the ampl model create the matrix 

import numpy as np
import os

#function to load npz and create dat file
def convertFile(in_filename,out_filename):
    dataset = np.load(in_filename+'.npz',allow_pickle=True)
    m = dataset['m']
    subsets = dataset['data']
    n = subsets.size

    #mxn matrix representation
    dataMatrix = np.zeros([m,n],dtype=bool)
    for j in range(n):
        subset = subsets[j]
        for i in subset:
            dataMatrix[i,j] = True

    #send to output
    with open(out_filename+'.dat', 'w') as f:
        f.write("param M:="+str(m)+";\n")
        f.write("param N:="+str(n)+";\n")
        f.write("param matr:=\n")
        for i in range(m):
            f.write("["+str(i)+",*]")
            for j in range(n):
                f.write(" "+str(j)+" "+str(int(dataMatrix[i,j])))
            f.write("\n")
        f.write(";")

#main function to convert all npz to dat files
if __name__ == '__main__':
    npz_folder = "benchmark"
    dat_folder = os.path.join("AMPL_export","benchmark_dat")

    for filename in os.listdir(npz_folder):  
        in_filename = os.path.join(npz_folder,filename.split('.')[0])
        out_filename = os.path.join(dat_folder,filename.split('.')[0])
        convertFile(in_filename,out_filename)