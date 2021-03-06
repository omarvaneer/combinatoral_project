import threading
import numpy as np
import random

class InstanceGeneration():
    def __init__(self):
        self.instance = None
        self.n = 0
        self.range = 0
    
    def generateRandomInstance(self,size, possVals, subsets):

        self.n = size
        self.range = possVals

        #create a full set continaing a range of possible values
        nums = range(possVals)
        trueSet = set(nums)#set(random.sample(nums,size))

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
            all_subsets.append(remainder)

        all_subsets= np.array([np.array(set) for set  in all_subsets])
        self.instance = all_subsets

        # print(trueSet)
        # print("____________________")
        # print(all_subsets)
    def toNPZ(self,instanceNum):
        with open('benchmark/r' + str(instanceNum) +'.npz', 'wb') as f0:
            np.savez(f0,m=self.range,data=self.instance)


if __name__ == '__main__':

    for i in range(1, 51):

        size = random.randint(1,3)
        if size == 1:
            instance = InstanceGeneration()
            num = random.randint(6,20)
            instance.generateRandomInstance(5+int(num/20), num, random.randint(int(2.5*num),int(3.5*num)))
            instance.toNPZ(i)
        elif size == 2:
            instance = InstanceGeneration()
            num = random.randint(21,100)
            instance.generateRandomInstance(5+int(num/20), num, random.randint(int(2.5*num),int(3.5*num)))
            instance.toNPZ(i)
        else:
            instance = InstanceGeneration()
            num = random.randint(101,300)
            instance.generateRandomInstance(5+int(num/20), num, random.randint(int(2.5*num),int(3.5*num)))
            instance.toNPZ(i)
        