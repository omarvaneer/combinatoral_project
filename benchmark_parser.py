import numpy as np
#import shutil #useful library for script automation/moving things around
import os

#the code might break if we give it corrupted text files or if the format is slightly different
#there are some checks to make sure the expected data is found but its not the most rigorous

def parseFile(in_filename,out_filename):
    file = open(in_filename+'.txt', "r")

    #first line
    m,n = list(map(int,file.readline().split()))
    dataMatrix = np.zeros([m,n],dtype=bool)
    #print(m)
    #print(n)

    #skip column weights
    counter = 0
    line = file.readline().split()
    while counter<n:
        counter += len(line)
        line = file.readline().split()

    #read data (m number of rows)
    for row in range(m):
        #number of col entries expected
        num_cols = int(line[0])
        i=0
        
        #populate mxn data matrix
        while i<num_cols:
            line = file.readline().split()
            indexes = list(map(int,line))
            for idx in indexes:
                #the indexes of raw data count starting from 1
                dataMatrix[row,idx-1]=True
            i+=len(indexes)
        
        #prepare next line
        line = file.readline().split()

    #print(dataMatrix)
    #double check end of file
    if(line):
        print("warning possibly bad file")

    #convert mxn matrix to list of lists representation
    data_list = []
    for col in range(n):
        subset = np.nonzero(dataMatrix[:,col])[0]
        data_list.append(subset)
    data=np.asarray(data_list,dtype=object)

    #two k values
    k1 = int(n/3)
    k2 = int(2*n/3)
    with open(out_filename+'_k'+str(k1)+'.npz', 'wb') as f0:
        np.savez(f0,m=m,k=k1,data=data)
    with open(out_filename+'_k'+str(k2)+'.npz', 'wb') as f1:
        np.savez(f1,m=m,k=k2,data=data)
    file.close()

if __name__ == '__main__':

    #raw folder of txt files
    raw_folder = "benchmark_raw"
    #processed npz files
    output_folder = "benchmark"

    for filename in os.listdir(raw_folder):
        in_filename = os.path.join(raw_folder,filename.split('.')[0])
        out_filename = os.path.join(output_folder,filename.split('.')[0])

        parseFile(in_filename,out_filename)
