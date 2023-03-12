# Jack McAllister  Student ID #: 001155294
# C950 Data Structures and Algorithms II
# NHP2 TASK 1: WGUPS ROUTING PROGRAM
# kdjfdlk
from package import Package
from myDictionary import MyDictionary
import csv

def checkDistance(double_dict, add1, add2):
    a = double_dict.get(add1).get(add2)
    b = double_dict.get(add2).get(add1)
    if a !=None:
        return a
    elif b!=None:
        return b
    else:
        return None

if __name__ == '__main__':

    with open('PackageFile_CSV.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        dict_of_packages = MyDictionary()
        for row in reader:
            id = int(row.get('Package ID'))
            address = row.get('Address')
            deadline = row.get('Delivery Deadline')
            notes = row.get('Special Notes')
            status = ''
            deliverytime = ''
            package = Package(id, address, deadline, notes, status, deliverytime)
            dict_of_packages.insert(id,package)
        for outerbox in range(0, len(dict_of_packages.hash_map)):
            for innerelement in range(0,len(dict_of_packages.hash_map[outerbox])):
                key_val = dict_of_packages.hash_map[outerbox][innerelement]
                #print(key_val)
        test_pkg = dict_of_packages.get(21)
        print(test_pkg.id)
    distanceTable = MyDictionary(12)
    names = []
    with open('DistanceTable.csv') as csvfile2:
        reader2 = csv.reader(csvfile2, delimiter=',')
        for row in reader2:
            name1 = (row[0].lstrip(" .asw")).rstrip(" .asw").replace("\n", "")
            names.append(name1)
            insideDict = MyDictionary(20)

            for col in range(0, len(names)):
                name2 = names[col]
                if row[col]!='':
                    insideDict.insert(name2, row[col+1])
            distanceTable.insert(name1, insideDict)
            print(insideDict)
    '''
    for i in range(distanceTable.myDictLength()):
        print(distanceTable[i].myDictLength())
        '''
    print(checkDistance(distanceTable, "1060 Dalton Ave S", "3060 Lester St"))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
