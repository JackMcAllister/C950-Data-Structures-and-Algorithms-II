from typing import Any
from random import randint


class MyDictionary(object):
    def __init__(self, bins=11):
        self.hash_map = [[] for _ in range(bins)]

    def hash_function(self, item):
        return hash(item) % 10

    def insert(self, key, value):
        keyvalpair = (key, value)
        hashval = self.hash_function(key)
        if self.containskey(key):
            # self.hash_map[hashval][key] = keyvalpair
            self.hash_map[hashval].append(keyvalpair)
        else:
            self.hash_map[hashval].append(keyvalpair)

    def get(self, key):
        try:
            hashval = self.hash_function(key)
            if len(self.hash_map[hashval]) == 0:
                return None
            innerindex = self.search(self.hash_map[hashval], key)
            if innerindex == -1:
                return None
            else:
                return self.hash_map[hashval][innerindex][1]
        except:
            return None

    def getValues(self):
        values = []
        for l in range(len(self.hash_map)):
            if self.hash_map[l] == [] or self.hash_map[l] == None or len(self.hash_map[l]) < 1:
                pass
            else:
                innerlist = self.hash_map[l]
                for i in range(len(innerlist)):
                    item = innerlist[i]
                    values.append(item[1])
        return values

    def __str__(self) -> str:
        returnValue = ''

        for box in self.hash_map:
            if len(box) > 0:
                for tup in box:
                    returnValue += "{} : {}\n".format(tup[0], tup[1])
        return returnValue

    def myDictLength(self, key):
        dictLength = len(self.hash_map[self.hash_function(key)])
        return dictLength

    def search(self, list, search):

        found = False
        count = 0
        for item in list:
            if item[0] == search:
                found = True
            if found == True:
                return count
            count += 1
        return -1

    # not used
    def binarysearch(self, arr, search):
        length = int(len(arr))
        # length = self.myDictLength(search)
        low = 0
        '''
        if len(arr) is tuple:
            high = len(arr)[1]
        else:
            high = len(arr)
        '''
        mid = (length + low) // 2

        while low != length and low != mid and mid != length:
            if search > arr[mid][0]:
                low = mid + 1
                mid = (low + length) // 2
            elif search < arr[mid][0]:
                length = mid - 1
                mid = (low + length) // 2
            elif search == arr[mid][0]:
                return mid
        return None

    # not used
    def quicksort(self, arr):  # not implemented
        if len(arr) < 2:
            return arr
        low, same, high = [], [], []
        pivot = arr[randint(0, len(arr) - 1)]
        for index in arr:
            if index < pivot:
                low.append(index)
            elif index == pivot:
                same.append(index)
            elif index > pivot:
                high.append(index)
        return self.quicksort(low) + same + self.quicksort(high)

    def containskey(self, key):
        if self.get(key) == None:
            return False
        else:
            return True
