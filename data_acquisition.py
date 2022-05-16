import numpy as np
import random

class InstanceGeneration():
    def __init__(self):
        self.instance = None
    
    def readLiteratureData(self,fileName):
        pass

    def generateRandomInstance(self,size, possVals, subsets):
        
        #create a full set continaing a range of possible values
        nums = range(possVals)
        trueSet = set(random.sample(nums,size))

        #create a list of empty sets
        all_subsets = []
        subset_set = set()

        for i in range(subsets - 1):

            #create a subset of random size
            subset_size = random.randrange(size)
            
            #randomly grab values from true sets to create a subset
            one_subset = set(random.sample(trueSet,subset_size))
            one_subset_asarr = list(one_subset)

            #if the subset isnt empty, append it to the list
            if one_subset_asarr:
                all_subsets.append(one_subset_asarr)

                #create a set of all the subsets to ensure all values are grabbed
                subset_set = one_subset.union(subset_set)

        #if any values are missed, add them to the subset list as a subset
        remainder = trueSet.difference(subset_set)
        remainder = list(remainder)

        if len(remainder) != 0:
            subset_set.append(remainder)

        subset_set = np.array([np.array(set) for set  in subset_set])
        self.instance = subset_set
        
        # print(trueSet)
        # print("____________________")
        # print(all_subsets)


if __name__ == '__main__':

    test = InstanceGeneration()
    test.generateRandomInstance(10,100,10)


        