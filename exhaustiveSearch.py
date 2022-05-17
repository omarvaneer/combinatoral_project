from socket import timeout
import numpy as np
import multiprocessing
import os
import time

#The minimum set covering problem can be framed as an mxn array. M total elements in set (rows), N subsets (cols)

class ExhaustiveSearch():
    def __init__(self,dataFile):

        #load instance
        dataset = np.load(dataFile,allow_pickle=True)
        self.m = dataset['m']#total unique elements of set
        self.data = dataset['data']#array of subsets
                                    # if we want to introduce randomness in exhaustive search order,
                                    # I suggest adding a shuffle function to the dataset
        self.n = self.data.size #number of subsets
        self.k=dataset['k'] #number of subsets threshold

        #combination generator initial condition  
        self.subset_group = np.zeros(self.k,dtype=int)
        self.coolex_b = np.zeros(self.n,dtype=bool)
        for i in range(self.k):
            self.subset_group[i] = i
            self.coolex_b[i]=True
        self.coolex_x = int(self.k)
        self.coolex_y = int(self.k)

    #check a different combination
    def iterate(self):
        #check first
        if self.validateSets(self.subset_group):
            return 1 #found
        else:
            if self.coolex_x<self.n:
                #otherwise prepare the next combination
                self.nextCombination()
                return 0 #continue
            else:
                #combination generator has exhausted all combinations
                return -1 #terminate


    #cool-lex combination generation algorithm from 
    #https://www.sciencedirect.com/science/article/pii/S0012365X07009570
    def nextCombination(self):
        self.coolex_b[self.coolex_x-1] = False
        self.coolex_b[self.coolex_y-1] = True
        self.coolex_b[0] = self.coolex_b[self.coolex_x]
        self.coolex_b[self.coolex_x] = 1
        self.coolex_x = self.coolex_x+1-(self.coolex_x-1)*self.coolex_b[1]*(1-self.coolex_b[0])
        self.coolex_y=self.coolex_b[0]*self.coolex_y+1
        
        self.subset_group=np.nonzero(self.coolex_b)[0]

    #validation function
    #linearly look through all the subsets 
    def validateSets(self,subset_idxs):
        checkSet = np.zeros(self.m,dtype=bool)

        #check all subsets
        for s in range(self.k):
            subset = self.data[subset_idxs[s]]
            for i in range(subset.size):
                checkSet[subset[i]] = True

        #logical AND across all elements
        #if any of the elements in this array is zero, 
        #then there is an element that is not covered by the subsets
        return np.all(checkSet)

        #could add more checks for early termination.
        #its more likely that the guess returns false/worst case where the alg must go through all the subsets anyways
        #so the early termination wouldn't be worth the extra overhead

#this runs the algorithm in a function that can be put in its own process
def iterateExhaustiveSearch(e,result,num):
    with multiprocessing.get_context("spawn").Pool() as pool:
        #exhaustive search loop
        while (result==0):
            result = e.iterate()
            #print("in loop")

        #algorithm termination (not timeout)
        if(result==1):
            #print("minimum cover found")
            #print(e.subset_group)
            num.value=1
            #queue.put(e.subset_group)
        else:
            #print("no minimum cover")
            num.value=0

#creates an output file to log results of one run
def createOutputFile(filename, code):
    with open(filename, 'w') as f:
        f.write(str(code))
        #if code==1:
        #    f.write('\n')
        #    for idx in args:
        #        f.write(str(idx)+' ')

#runs one dataset for 1 minute and 10 minutes
def searchDataset(in_filename,out_filename,time):

    e = ExhaustiveSearch(in_filename+'.npz')
    num = multiprocessing.Value('i', 0)
    #arr = multiprocessing.lis('i', range(e.k))

    result = e.iterate()
    p=multiprocessing.Process(target=iterateExhaustiveSearch,args=[e,result,num])
    p.start()
    p.join(time)#run for 60 seconds or 600 seconds before timeout

    #check timeout
    if p.is_alive():
        p.terminate()
        #print("timeout - minimum cover not found")
        createOutputFile(out_filename+'_t'+str(time)+'.txt',2)
    else:
        if num.value==0:
            createOutputFile(out_filename+'_t'+str(time)+'.txt',0)
        else:
            createOutputFile(out_filename+'_t'+str(time)+'.txt',1) #consider adding array/certificate

#main event loop with timeout
if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    #folder of benchmark npz files
    benchmark_folder = "benchmark"
    output_folder = "exhaustive_output"

    for filename in os.listdir(benchmark_folder):
        print(filename)
        in_filename = os.path.join(benchmark_folder,filename.split('.')[0])
        out_filename = os.path.join(output_folder,filename.split('.')[0])

        searchDataset(in_filename,out_filename,60) #1 minute
        searchDataset(in_filename,out_filename,600) #10 minutes



