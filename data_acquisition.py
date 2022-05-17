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
            all_subsets.append(remainder)

        all_subsets= np.array([np.array(set) for set  in all_subsets])
        self.instance = all_subsets

        # print(trueSet)
        # print("____________________")
        # print(all_subsets)
    def toNPZ(self,instanceNum):
        k1 = int((self.n)/3)
        k2 = int(2*(self.n)/3)
        with open('benchmark/r' + str(instanceNum) +'_k'+ str(k1)+'.npz', 'wb') as f0:
            np.savez(f0,m=self.range,k=k1,data=self.instance)
        with open('benchmark/r' + str(instanceNum) +'_k'+ str(k2)+'.npz', 'wb') as f1:
            np.savez(f1,m=self.range,k=k2,data=self.instance)


if __name__ == '__main__':

    for i in range(1, 26):

        size = random.randint(1,3)
        if size == 1:
            instance = InstanceGeneration()
            num = random.randint(10,15)
            instance.generateRandomInstance(num, num * 10, num - random.randint(1,5))
            instance.toNPZ(i)
        elif size == 2:
            instance = InstanceGeneration()
            num = random.randint(16,100)
            instance.generateRandomInstance(num, num * 10, abs(num - random.randint(5,45)))
            instance.toNPZ(i)
        else:
            instance = InstanceGeneration()
            num = random.randint(101,1001)
            instance.generateRandomInstance(num, num * 10, abs(num - random.randint(45,95)))
            instance.toNPZ(i)
        