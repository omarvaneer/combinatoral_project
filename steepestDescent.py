#similar to the uniform graph partition example problem
import numpy as np
import copy

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
    def __fullyCovered(self):
        return np.all(self.__coveredSet)
    #adds a subset to the group of subsets
    def __addSubset(self, subsetidx):
        self.__subsetGroup.append(subsetidx)
        self.__selectedSubsets[subsetidx]=1
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

    def greedyInit(self):
        while(~self.__fullyCovered()):
            idx = self.__findMaxUncoveredIdx()
            if idx==-1: #shouldn't happen
                return -1
            self.__addSubset(idx)
        return self.__k
    
    #find a 2-opt like neighbor in linear time
    def getNeighbor(self, selectedSubsets,i,j):
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
        neighbor = selectedSubsets
        neighbor[i_idx]=0
        neighbor[j_idx]=1
        return neighbor

    #evaluate quality of neighbor
    def getNumUncovered(self,selectedSubsets):
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
    def improve(self):
    #loop through all 2-opt neighbors
        k=self.__k
        n=self.__n
        subsets = self.__selectedSubsets
        championSubset = subsets
        minUncovered = self.getNumUncovered(championSubset)
            
        #k 1s, n-k 0s
        #choose 1 from each group to swap
        for i in range(k):
            for j in range(n-k):
                neighbor =self.getNeighbor(subsets,i,j)
                #evaluate performance
                numUncovered = self.getNumUncovered(neighbor)
                #shortcut
                if numUncovered==0:
                    return neighbor
                #track the minimum
                if numUncovered<minUncovered:
                    minUncovered=numUncovered
                    championSubset=neighbor
        #return best neighbor
        return championSubset

    #randomly delete one element
    def decreaseK(self):
        ones_idx = self.rng.integers(self.__k)
        for idx in range(len(self.__selectedSubsets)):
            #if that subset is selected
            if self.__selectedSubsets[idx]:
                self.__selectedSubsets[idx]=0
                self.__k-=1
                return idx

    #loop to get to 2-optimal solution
    def minimizeUncovered(self):
        #minimize uncovered elements
        current = self.__selectedSubsets
        next = self.improve()
        while not np.array_equiv(current,next):
            print(current)
            current = next
            next = self.improve()
        self.__selectedSubsets = current
        return self.getNumUncovered(current)

    #get min k using steepest descent
    def descentLoop(self):
        #linear search approach for k
        #choose k
        #get initial sol
        #run steepest descent to minimize uncovered elements
        #if min is 0, decrease k
        #if min is not 0, end and return last k
        self.greedyInit()
        uncovered = self.minimizeUncovered()
        champion = np.zeros(self.__n,dtype=bool)
        while uncovered==0:
            champion = copy.deepcopy(self.__selectedSubsets)
            self.decreaseK()
            uncovered = self.minimizeUncovered()     

        self.__selectedSubsets=champion #data stored before k was decreased
        return self.__k+1 #make up for the last call to decreaseK
    
    def readSolution(self):
        return self.__selectedSubsets

if __name__ == '__main__':
    s = steepestDescentSearch("benchmark/h1.npz")
    k = s.descentLoop()
    sol = s.readSolution()
    print(k)
    print(sol)