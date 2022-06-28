#similar to the uniform graph partition example problem
#minimizes uncovered elements using local search, then decreases k

#the results don't really show improvement over the greedy solution
#it seems like simple 2-opt neighborhood is too small so it gets stuck in a local minimum too easily 

import numpy as np
import copy
import os
import multiprocessing
import time

class steepestDescentSearch():
    def __init__(self,dataFile):
        #load instance
        dataset = np.load(dataFile,allow_pickle=True)
        self.__m = dataset['m']#total unique elements of set
        self.__data = dataset['data']#array of subsets
        self.__n = self.__data.size #number of subsets

        self.__coveredSet = np.zeros(self.__m,dtype=bool)
        self.__selectedSubsets = np.zeros(self.__n,dtype=bool)
        self.__subsetGroup = []
        self.__k= 0 
        self.rng = np.random.default_rng()
        #returns true if the true set is fully covered

    #functions from Greedy Search
    def __g_fullyCovered(self):
        return np.all(self.__coveredSet)

    #adds a subset to the group of subsets
    def __g_addSubset(self, subsetidx):
        self.__subsetGroup.append(subsetidx)
        self.__selectedSubsets[subsetidx]=1
        self.__k+=1
        subset = self.__data[subsetidx]
        for i in range(subset.size):
            self.__coveredSet[subset[i]] = True
    #finds the number of uncovered elements in a subset
    def __g_numUncovered(self, subsetidx):
        subset = self.__data[subsetidx]
        uncovered = 0
        for i in range(subset.size):
            if self.__coveredSet[subset[i]] == False:
                uncovered+=1
        return uncovered
    #finds the subset with the most uncovered elements
    def __g_findMaxUncoveredIdx(self):
        max = 0
        maxidx = -1
        for subsetidx in range(self.__n):
            x = self.__g_numUncovered(subsetidx)
            if x>max:
                max = x
                maxidx = subsetidx
        return maxidx

    #start using greedy solution
    def __greedyInit(self):
        while(~self.__g_fullyCovered()):
            idx = self.__g_findMaxUncoveredIdx()
            if idx==-1: #shouldn't happen
                return -1
            self.__g_addSubset(idx)
        return self.__k

    #starts at k=n trivial solution
    def __full_init(self):
        self.__k=self.__n
        self.__selectedSubsets = np.ones(self.__n, dtype=bool)
    
    #find a 2-opt like neighbor in linear time
    def __getNeighbor(self, selectedSubsets,i,j):
        i_idx=0
        j_idx=0
        ones = 0
        zeros = 0

        #find index to swap
        for idx in range(len(selectedSubsets)):
            #is 1
            if selectedSubsets[idx]:
                if ones==i: i_idx=idx
                ones+=1
            else:
                if zeros==j: j_idx=idx
                zeros+=1

        #swap
        neighbor = copy.deepcopy(selectedSubsets)
        neighbor[i_idx]=0
        neighbor[j_idx]=1
        return neighbor

    #evaluate quality of neighbor
    def __getNumUncovered(self,selectedSubsets):
        m = self.__m
        coveredSet = np.zeros(m,dtype=bool)
        for idx in range(len(selectedSubsets)):
            #if that subset is selected
            if selectedSubsets[idx]:
                subset = self.__data[idx]
                for i in range(subset.size):
                    coveredSet[subset[i]] = True
        return m - np.sum(coveredSet)

    #go to best 2-opt neighbor
    def __improve(self):
    #loop through all 2-opt neighbors
        k=self.__k
        n=self.__n
        subsets = self.__selectedSubsets
        championSubset = copy.deepcopy(subsets)
        minUncovered = self.__getNumUncovered(championSubset)
        if minUncovered==0: return subsets
        #k 1s, n-k 0s
        #choose 1 from each group to swap
        for i in range(k):
            for j in range(n-k):
                neighbor =self.__getNeighbor(subsets,i,j)
                #evaluate performance
                numUncovered = self.__getNumUncovered(neighbor)
                #shortcut
                if numUncovered==0:
                    return neighbor
                #track the minimum
                if numUncovered<minUncovered:
                    minUncovered=numUncovered
                    championSubset=neighbor
        #return best neighbor
        return championSubset

    #randomly delete one element from last solution
    def __decreaseK(self):
        ones_idx = self.rng.integers(self.__k)
        for idx in range(len(self.__selectedSubsets)):
            #if that subset is selected
            if self.__selectedSubsets[idx]:
                self.__selectedSubsets[idx]=0
                self.__k-=1
                return idx

    #fully random version
    def __decreaseK_r(self):
        self.__k-=1
        self.__selectedSubsets=np.zeros(self.__n, dtype=bool)
        ones = set()
        while (len(ones)<self.__k):
            ones.add(self.rng.integers(self.__n))

        for idx in ones:
            self.__selectedSubsets[idx]=1
        return 0

    #loop to get to 2-optimal solution
    def __minimizeUncovered(self,iterations):
        #minimize uncovered elements
        current = copy.deepcopy(self.__selectedSubsets)
        next = self.__improve()
        while not np.array_equiv(current,next):
            iterations.value = iterations.value+1
            current = next
            next = self.__improve()
        self.__selectedSubsets = current
        return self.__getNumUncovered(current)

    #get min k using steepest descent
    def descentLoop(self,num,iterations):
        iterations.value=0        
        #self.__greedyInit()
        self.__full_init()
        uncovered = self.__minimizeUncovered(iterations)
        champion = np.zeros(self.__n,dtype=bool)
        while uncovered==0:
            num.value = int(self.__k)
            champion = copy.deepcopy(self.__selectedSubsets)
            self.__decreaseK_r()
            uncovered = self.__minimizeUncovered(iterations)    
            #print("uncovered elements = "+str(uncovered))
            #print("with k = " +str(self.__k))

        self.__selectedSubsets=champion #data stored before k was decreased
        return self.__k+1 #make up for the last call to decreaseK
    
    def readSolution(self):
        return self.__selectedSubsets

#creates an output file to log results of one run
def createOutputFile(filename, code,mink):
    with open(filename, 'w') as f:
        f.write(str(code))
        f.write('\n')
        if code!=-1:
            f.write(str(mink))
        else:
            f.write(str(-1))

def createMetadataFile(filename, runtime, iterations):
    with open(filename, 'w') as f:
        f.write(str(runtime))
        f.write('\n')
        f.write(str(iterations))


#wrapper function for multiprocessing library interface
def runFindMinK(in_filename,exitcode,num,iterations):
    s = steepestDescentSearch(in_filename+'.npz')
    result = s.descentLoop(num,iterations)
    exitcode.value = int(result!=0)

#creates an output file to log results of one run
def createOutputFile(filename, code,mink):
    with open(filename, 'w') as f:
        f.write(str(code))
        f.write('\n')

        if code!=-1:
            f.write(str(mink))
        else:
            f.write(str(-1))
        #    for idx in args:
        #        f.write(str(idx)+' ')

#runs one dataset for 1 minute and 10 minutes
def steepestDescentSearchDataset(in_filename,out_filename,out_filename2,rtime):

    exitcode = multiprocessing.Value('i', 0)
    mink = multiprocessing.Value('i', 0)
    iterations = multiprocessing.Value('i', 0)

    #arr = multiprocessing.lis('i', range(e.k))

    p=multiprocessing.Process(target=runFindMinK,args=[in_filename,exitcode,mink,iterations])
    tic = time.perf_counter()
    toc=tic
    p.start()
    p.join(rtime)#run for 60 seconds or 600 seconds before timeout

    #check timeout
    if p.is_alive():
        p.terminate()
        toc = time.perf_counter()
        #print("timeout - minimum cover not found")
        createOutputFile(out_filename+'_t'+str(rtime)+'.txt',0, mink.value)
    else:
        toc = time.perf_counter()
        createOutputFile(out_filename+'_t'+str(rtime)+'.txt',exitcode.value,mink.value)
        
    runtime = toc-tic
    createMetadataFile(out_filename2+'_t'+str(rtime)+'.txt',iterations.value, runtime)

#main event loop with timeout
if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    #folder of benchmark npz files
    benchmark_folder = "benchmark"
    output_folder = "steepestDescent_r_output"
    output_folder2 = "steepestDescent_r_output2"

    for filename in os.listdir(benchmark_folder):
        
        print(filename)
        in_filename = os.path.join(benchmark_folder,filename.split('.')[0])
        out_filename = os.path.join(output_folder,filename.split('.')[0])
        out_filename2 = os.path.join(output_folder2,filename.split('.')[0])

        steepestDescentSearchDataset(in_filename,out_filename,out_filename2,60) #1 minute
        #steepestDescentSearchDataset(in_filename,out_filename,out_filename2,600) #10 minutes
