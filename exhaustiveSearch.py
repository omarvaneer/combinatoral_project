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
        self.__m = dataset['m']#total unique elements of set
        self.__data = dataset['data']#array of subsets
                                    # if we want to introduce randomness in exhaustive search order,
                                    # I suggest adding a shuffle function to the dataset
        self.__n = self.__data.size #number of subsets
        self.__k= self.__n #initial k threshold = n

        #combination generator initial condition  
        self.__subset_group = np.zeros(self.__k,dtype=int)
        self.__coolex_b = np.zeros(self.__n,dtype=bool)
        for i in range(self.__k):
            self.__subset_group[i] = i
            self.__coolex_b[i]=True
        self.__coolex_x = int(self.__k)
        self.__coolex_y = int(self.__k)
    
    #resets the combination generator for different k
    def reset_k(self, k):
        if (k>self.__n):
            print("ERROR K>N")
        self.__k=int(k)#dataset['k'] #number of subsets threshold
        self.__subset_group = np.zeros(self.__k,dtype=int)
        self.__coolex_b = np.zeros(self.__n,dtype=bool)
        for i in range(self.__k):
            self.__subset_group[i] = i
            self.__coolex_b[i]=True
        self.__coolex_x = int(self.__k)
        self.__coolex_y = int(self.__k)

    #check a different combination
    def __iterate(self):
        #check first
        if self.__validateSets(self.__subset_group):
            return 1 #found
        else:
            if self.__coolex_x<self.__n:
                #otherwise prepare the next combination
                self.__nextCombination()
                return 0 #continue
            else:
                #combination generator has exhausted all combinations
                return -1 #terminate

    #cool-lex combination generation algorithm from 
    #https://www.sciencedirect.com/science/article/pii/S0012365X07009570
    def __nextCombination(self):
        self.__coolex_b[self.__coolex_x-1] = False
        self.__coolex_b[self.__coolex_y-1] = True
        self.__coolex_b[0] = self.__coolex_b[self.__coolex_x]
        self.__coolex_b[self.__coolex_x] = 1
        self.__coolex_x = self.__coolex_x+1-(self.__coolex_x-1)*self.__coolex_b[1]*(1-self.__coolex_b[0])
        self.__coolex_y=self.__coolex_b[0]*self.__coolex_y+1
        
        self.__subset_group=np.nonzero(self.__coolex_b)[0]

    #validation function
    #linearly look through all the subsets 
    def __validateSets(self,subset_idxs):
        checkSet = np.zeros(self.__m,dtype=bool)

        #check all subsets
        for s in range(self.__k):
            subset = self.__data[subset_idxs[s]]
            for i in range(subset.size):
                checkSet[subset[i]] = True

        #logical AND across all elements
        #if any of the elements in this array is zero, 
        #then there is an element that is not covered by the subsets
        return np.all(checkSet)

        #could add more checks for early termination.
        #its more likely that the guess returns false/worst case where the alg must go through all the subsets anyways
        #so the early termination wouldn't be worth the extra overhead
    
    def __runExhaustiveSearch(self):
        result = self.__iterate()
        while (result==0):
            result = self.__iterate()
        return result

    def getk(self):
        return self.__k

    def find_min_k(self,num):  
        #k=n
        result = self.__runExhaustiveSearch()
        if result==-1:
            return -1
        else:
            num.value=self.getk()
            #binary search
            #done not iteratively so that num.value can be updated easily
            kmax = self.getk()
            kmin = 1
            kcurrent = np.floor(kmax/2) 
            while (kmin!=kmax):
                self.reset_k(kcurrent)
                result = self.__runExhaustiveSearch()
                if result==1:
                    kmax = kcurrent
                    num.value = int(kmax)
                    kcurrent = np.floor((kmax+kmin)/2) 
                else:
                    kmin = kcurrent+1
                    kcurrent = np.floor((kmax+kmin)/2) 
            num.value = int(kmax)
            return 1


#wrapper function for multiprocessing library interface
def runFindMinK(in_filename,exitcode,num):
    e = ExhaustiveSearch(in_filename+'.npz')
    result = e.find_min_k(num)
    exitcode.value = result

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
def searchDataset(in_filename,out_filename,time):

    exitcode = multiprocessing.Value('i', 0)
    mink = multiprocessing.Value('i', 0)
    #arr = multiprocessing.lis('i', range(e.k))

    p=multiprocessing.Process(target=runFindMinK,args=[in_filename,exitcode,mink])
    p.start()
    p.join(time)#run for 60 seconds or 600 seconds before timeout

    #check timeout
    if p.is_alive():
        p.terminate()
        #print("timeout - minimum cover not found")
        createOutputFile(out_filename+'_t'+str(time)+'.txt',0, mink.value)
    else:
        createOutputFile(out_filename+'_t'+str(time)+'.txt',exitcode.value,mink.value)
        

#main event loop with timeout
if __name__ == '__main__':
    multiprocessing.set_start_method("spawn")
    #folder of benchmark npz files
    benchmark_folder = "benchmark"
    output_folder = "exhaustive_output"

    for filename in os.listdir(benchmark_folder):
        if filename[3]=='e':
            print(filename)
            in_filename = os.path.join(benchmark_folder,filename.split('.')[0])
            out_filename = os.path.join(output_folder,filename.split('.')[0])

            searchDataset(in_filename,out_filename,60) #1 minute
            searchDataset(in_filename,out_filename,600) #10 minutes

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
