# Jack McAllister  Student ID #: 001155294
# C950 Data Structures and Algorithms II
# NHP2 TASK 1: WGUPS ROUTING PROGRAM

from package import Package
from truck import Truck
from myDictionary import MyDictionary
import csv
import re


def checkDistance(double_dict, add1, add2):
    a = double_dict.get(add1).get(add2)
    b = double_dict.get(add2).get(add1)
    if a != None:
        return a
    elif b != None:
        return b
    else:
        return None


def sortPackages(allPackages):
    # algorithm takes a list (allPackages) and sorts into 3 truckLoads (#of trucks we have)
    allPKGList = allPackages.getValues()
    groupPackageIDs = set()  # adds id to set to then add to group pkgs
    groupedPackages = []
    truckList1 = []
    truckList2 = []
    truckList3 = []

    for package in allPKGList:  # finds all 'grouped together req' packages
        if package.deliveredWithReq is not None:
            groupedPackages.append(package)
            allPKGList.remove(package)
            for id in package.deliveredWithReq:
                groupPackageIDs.add(id)

    for package in allPKGList:  # finds pgk ids in grouped required list from allPKGList to groupedPackages
        if package.id in groupPackageIDs:
            groupedPackages.append(package)
            allPKGList.remove(package)

    for package in allPKGList:  # assign truck number requirement
        if package.truckReq == 1:
            truckList1.append(package)
            allPKGList.remove(package)
        elif package.truckReq == 2:
            truckList2.append(package)
            allPKGList.remove(package)
        elif package.truckReq == 3:
            truckList3.append(package)
            allPKGList.remove(package)
        elif package.truckReq is None:
            pass

    for package in allPKGList:  # assign delayed packages to truck number 2 if it can fit
        if package.delayedReq:
            if 16 - len(truckList2) > 0:
                truckList2.append(package)
                allPKGList.remove(package)
            elif 16 - len(truckList3) > 0:
                truckList3.append(package)
                allPKGList.remove(package)
            elif 16 - len(truckList1) > 0:
                truckList1.append(package)
                allPKGList.remove(package)
            else:
                print("delayed package can't fit on truck")

    if (16 - len(truckList1)) > len(groupedPackages):  # add groupedPackages to truckList if it can fit
        for package in groupedPackages:
            truckList1.append(package)
    elif (16 - len(truckList2)) > len(groupedPackages):
        for package in groupedPackages:
            truckList2.append(package)
    elif (16 - len(truckList3)) > len(groupedPackages):
        for package in groupedPackages:
            truckList3.append(package)
    else:
        print("Grouped Packages can not be added to a single truck")

    for package in allPKGList:  # add other packages to truck lists
        canFit1 = 16 - len(truckList1) > 0
        canFit2 = 16 - len(truckList2) > 0
        canFit3 = 16 - len(truckList3) > 0
        if canFit1:
            truckList1.append(package)
            # allPKGList.remove(package)
        elif canFit2:
            truckList2.append(package)
            # allPKGList.remove(package)
        elif canFit3:
            truckList3.append(package)
            # allPKGList.remove(package)

    truckLoads = [truckList1, truckList2, truckList3]
    # set of lists, 1 list for each truck: [[pkgid, [pgkid],[pkgid], ...]
    # print('truckList1 :', len(truckList1), truckList1, '\n', 'truckList2 :', len(truckList2), truckList2, '\n',
    #      'truckList3 :', len(truckList3), " ", truckList3)
    return truckLoads


def convertTime(rawVal):
    time_pattern = re.compile(r'[^0-9]')
    # if the raw value contains a non-decimal character
    # then remove non-decimal characters and convert to int
    if rawVal != "EOD":
        rawVal = re.sub('[^0-9]', '', rawVal)
        return rawVal
    else:
        return 2400


def loadPackages():
    with open('PackageFile_CSV.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        dict_of_packages = MyDictionary()
        packageList = []
        for row in reader:
            id = int(row.get('Package ID'))
            address = row.get('Address')
            deadline = row.get('Delivery Deadline')
            deadline = convertTime(deadline)
            notes = row.get('Special Notes')
            status = 'At Hub'

            package = Package(id, address, deadline, notes, status)
            dict_of_packages.insert(id, package)

            # packageList = packageList.append(dict_of_packages.index(0))

        for outerbox in range(0, len(dict_of_packages.hash_map)):
            for innerelement in range(0, len(dict_of_packages.hash_map[outerbox])):
                key_val = dict_of_packages.hash_map[outerbox][innerelement]
                # print(key_val)
        test_pkg = dict_of_packages.get(21)
        print(test_pkg.id)
        print(test_pkg.deadline)
        return dict_of_packages


def loadDistances():
    distances = MyDictionary(12)
    names = []
    with open('DistanceTable.csv') as csvfile2:
        reader2 = csv.reader(csvfile2, delimiter=',')
        for row in reader2:
            name1 = (row[0].lstrip(" .asw")).rstrip(" .asw").replace("\n", "")
            names.append(name1)
            insideDict = MyDictionary(20)

            for col in range(0, len(names)):
                name2 = names[col]
                if row[col] != '':
                    insideDict.insert(name2, row[col + 1])
            distances.insert(name1, insideDict)
            # print(insideDict)
        return distances


if __name__ == '__main__':
    packages = loadPackages()
    distanceTable = loadDistances()
    loads = sortPackages(packages)
    trucks = []
    index = 1
    for load in loads:
        if index == 1:
            start = 800
        elif index == 2:
            start = 905
        truck = Truck(index, load, start)
        trucks.append(truck)
        index += 1

    for truck in trucks:
        truck.findRoute(distanceTable)
        print("Truck ID:", truck.id, "\nNumber of Packages:", len(truck.packageList))
        print("Total Distance:", truck.totalDistance, "\nEOD Time:", truck.EODTime)
        truck.failedDelivery()
        print("\n\n")


    # print(input"what package are you looking for? what time is it now?")
    #  format time "XX:XX"
    #  package 21 is en route at 9am.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
