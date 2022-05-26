import numpy as np
import multiprocessing
import os

#greedy approach to add subsets with the greatest uncovered elements until the true set is fully covered

class GreedySearch():
    def __init__(self,dataFile):
        #load instance
        dataset = np.load(dataFile,allow_pickle=True)
        self.__m = dataset['m']#total unique elements of set
        self.__data = dataset['data']#array of subsets
        self.__n = self.__data.size #number of subsets

        self.__coveredSet = np.zeros(self.__m,dtype=bool)
        self.__subsetGroup = []
        self.__k= 0 

    #returns true if the true set is fully covered
    def __fullyCovered(self):
        return np.all(self.__coveredSet)

    #adds a subset to the group of subsets
    def __addSubset(self, subsetidx):
        self.__subsetGroup.append(subsetidx)
        self.__k+=1
        subset = self.__data[subsetidx]
        for i in range(subset.size):
            self.__coveredSet[subset[i]] = True

    #finds the number of uncovered elements in a subset
    def __numUncovered(self, subsetidx):
        subset = self.__data[subsetidx]
        uncovered = 0
        for i in range(subset.size):
            if self.__coveredSet[subset[i]] == False:
                uncovered+=1
        return uncovered
    
    #finds the subset with the most uncovered elements
    def __findMaxUncoveredIdx(self):
        max = 0
        maxidx = -1
        for subsetidx in range(self.__n):
            x = self.__numUncovered(subsetidx)
            if x>max:
                max = x
                maxidx = subsetidx
        return maxidx

    #implements the greedy algorithm
    def runGreedySearch(self,exitcode):
        while(~self.__fullyCovered()):
            idx = self.__findMaxUncoveredIdx()
            if idx==-1: #shouldn't happen
                exitcode.value = -1 
                return -1
            self.__addSubset(idx)
        exitcode.value = 1 #successful termination code
        return self.__k

#wrapper function for multiprocessing library interface
def runFindMinKGreedy(in_filename,exitcode,k):
    g = GreedySearch(in_filename+'.npz')
    k.value = g.runGreedySearch(exitcode)

#creates an output file to log results of one run
def createOutputFile(filename, code,mink):
    with open(filename, 'w') as f:
        f.write(str(code))
        f.write('\n')
        if code!=-1:
            f.write(str(mink))
        else:
            f.write(str(-1))

#runs one dataset for 10 minutes
#greedy really shouldn't take that long. just placing an upper timeout bound for consistency
def searchDataset(in_filename,out_filename,time):

    exitcode = multiprocessing.Value('i', 0)
    mink = multiprocessing.Value('i', 0)

    p=multiprocessing.Process(target=runFindMinKGreedy,args=[in_filename,exitcode,mink])
    p.start()
    p.join(time)

    #check timeout
    if p.is_alive():
        p.terminate()
        createOutputFile(out_filename+'_t'+str(time)+'.txt',0, mink.value)
    else:
        createOutputFile(out_filename+'_t'+str(time)+'.txt',exitcode.value,mink.value)
        
#main event loop with timeout
if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    #folder of benchmark npz files
    benchmark_folder = "benchmark"
    output_folder = "greedy_output"

    for filename in os.listdir(benchmark_folder):
        print(filename)
        in_filename = os.path.join(benchmark_folder,filename.split('.')[0])
        out_filename = os.path.join(output_folder,filename.split('.')[0])

        searchDataset(in_filename,out_filename,600) #10 minutes
        #in practice, each run takes at most like 15 seconds

"""
output file format:
    row1: exit code
        1: optimal minimum k found
        -1: no set cover for any k
        0: timeout reached
    row2: k value
        if row1 == 1, k is optimal
        if row1 == 0, k is the best k found before timeout
        0: something went wrong. this shouldn't happen
        -1: no set cover for any k
"""
