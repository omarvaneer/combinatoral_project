import numpy as np
#mxn array. M total elements in set, N subsets

#if we want to introduce randomness in exhaustive search order, I suggest adding a shuffle function to the dataset

class ExhaustiveSearch():
    def __init__(self,dataFile,k):
        dataset = np.load(dataFile,allow_pickle=True)
        self.m = dataset['m']#total unique elements of set
        self.data = dataset['data']#array of subsets
        self.n = self.data.size #number of subsets
        self.k=int(np.min([k,self.data.size]))#number of subsets threshold

        #combination generator initial condition  
        self.subset_group = np.zeros(self.k,dtype=int)
        self.coolex_b = np.zeros(self.n,dtype=bool)
        for i in range(k):
            self.subset_group[i] = i
            self.coolex_b[i]=True
        self.coolex_x = int(k)
        self.coolex_y = int(k)

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
                return -1 #terminate


    #combination generation algorithm from 
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
        return np.all(checkSet)

        #could add more checks for early termination.
        #its more likely that the guess returns false/worst case where the alg must go through all the subsets anyways
        #so the early termination wouldn't be worth the extra overhead

        
#main event loop with timeout
if __name__ == '__main__':
    k=2
    e = ExhaustiveSearch('example.npz',k)
    result = e.iterate()

    while (result==0):
        result = e.iterate()

    if(result==1):
        print("minimum cover found")
        print(e.subset_group)
    else:
        print("minimum subset not found")