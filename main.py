# Jack McAllister  Student ID #: 001155294
# C950 Data Structures and Algorithms II
# NHP2 TASK 1: WGUPS ROUTING PROGRAM

from package import Package
from truck import Truck
from myDictionary import MyDictionary
import csv
import re


# Takes a list and two addresses
def checkDistance(double_dict, add1, add2):
    a = double_dict.get(add1).get(add2)
    b = double_dict.get(add2).get(add1)
    if a != None:
        return a
    elif b != None:
        return b
    else:
        return None


# goes through my list of packages and sorts them based on their delievery requirements
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
    for package in allPKGList:
        if package.wrongAddress:
            truckList3.append(package)
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
        if canFit1 and package.deadline < 2400:
            truckList1.append(package)
            allPKGList.remove(package)
        elif canFit2 and package.deadline < 2400:
            truckList2.append(package)
            allPKGList.remove(package)
        elif canFit3 and package.deadline < 2400:
            truckList3.append(package)
            allPKGList.remove(package)
    for package in allPKGList:  # add other packages to truck lists
        canFit1 = 16 - len(truckList1) > 0
        canFit2 = 16 - len(truckList2) > 0
        canFit3 = 16 - len(truckList3) > 0
        if canFit3:
            truckList3.append(package)
        elif canFit2:
            truckList2.append(package)
        elif canFit1:
            truckList1.append(package)

    truckLoads = [truckList1, truckList2, truckList3]

    return truckLoads


# this converts 'EOD' to '2400'
def convertTime(rawVal):
    time_pattern = re.compile(r'[^0-9]')
    # if the raw value contains a non-decimal character
    # then remove non-decimal characters and convert to int
    if rawVal != "EOD":
        rawVal = re.sub('[^0-9]', '', rawVal)
        return rawVal
    else:
        return 2400


# this loads my packages into a hashtable (myDictionary Object: dict_of_packages) from the Excel CSV file
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
            status = row.get('At Hub')
            zipcode = row.get('Zip')
            city = row.get('City ')
            state = row.get('State')
            weight = row.get('Mass KILO')

            package = Package(id, address, deadline, notes, status, zipcode, city, state, weight)
            dict_of_packages.insert(id, package)

            # packageList = packageList.append(dict_of_packages.index(0))

        for outerbox in range(0, len(dict_of_packages.hash_map)):
            for innerelement in range(0, len(dict_of_packages.hash_map[outerbox])):
                key_val = dict_of_packages.hash_map[outerbox][innerelement]
                # print(key_val)
        test_pkg = dict_of_packages.get(21)
        return dict_of_packages


# this creates a 'myDictionary hash table' with another 'myDictionary hash table' has its value
# the inner 'myDictionary hash table' object's value is the distance between the two addresses
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
        return distances


#  this is my package status lookup method
def packagestatuslookup(id, time):
    packageIDprompt = id  # (input("enter package ID number")
    packageIDprompt = int(packageIDprompt)
    Time_Prompt = time  # input("enter time of day in military time")
    Time_Prompt = re.sub('\D', '', Time_Prompt)
    Time_Prompt = int(Time_Prompt)
    pkgINQUIRY = packages.get(packageIDprompt)
    pkgINQUIRY_TRUCK_ID = pkgINQUIRY.onTruck
    Truck_with_Package = trucks[pkgINQUIRY_TRUCK_ID - 1]
    truck_departure_time = Truck_with_Package.departureTime

    print("Package ID:", pkgINQUIRY.id, "at time:", time)

    if truck_departure_time >= Time_Prompt:
        print("Status: At Hub,", "Deadline:", pkgINQUIRY.deadline)
    elif pkgINQUIRY.deliverytime > Time_Prompt:
        print("Status: En Route to Delivery Address,", "Deadline:", pkgINQUIRY.deadline)
    elif pkgINQUIRY.deliverytime <= Time_Prompt:
        print("Status:", pkgINQUIRY.status, ", Deadline:", pkgINQUIRY.deadline)
    print("Delivery Address:", pkgINQUIRY.address, ",", pkgINQUIRY.city, ",", pkgINQUIRY.state, ",",
          pkgINQUIRY.zipcode, "\nKilos:", pkgINQUIRY.weight, ",", "Notes:", pkgINQUIRY.notes)
    print("\nTotal distance traveled by 3 trucks:", totalDistance)
    return None


if __name__ == '__main__':
    packages = loadPackages()  # packages are loaded into a hash from the csv file
    distanceTable = loadDistances()  # distances are loaded into a nesting hast table from csv file
    loads = sortPackages(packages)  # packages are sorted into 3 lists based on requirements
    trucks = []  # truck list is instantiated
    allpkgList = []  # all package list is instantiated
    # packages = MyDictionary(24)
    index = 1
    for load in loads:  # the lists are loaded into the 3 trucks as the trucks are instantiated
        if index == 1:
            start = 800  # earliest a truck can leave the HUB
        elif index == 2:
            start = 906  # delayed packages on the flight, will not get to HUb until 9:05am
        truck = Truck(index, load, start)
        trucks.append(truck)
        index += 1

    index = 1
    # truck 3 leaves when the first of truck 1 or 2 gets back to the hub
    totalDistance = 0
    for truck in trucks:
        if index == 3:
            truck.departureTime = min(trucks[0].EODTime, trucks[1].EODTime)
        index += 1

        print("Truck ID:", truck.id, "\nNumber of Packages:", len(truck.packageList))
        truck.findRoute(distanceTable)
        print("Total Distance:", round(truck.totalDistance),
              "\n" "Start time:", truck.departureTime, "\nEOD Time:",
              truck.EODTime)
        totalDistance += truck.totalDistance  # add each truck's distance traveled
        truck.failedDelivery()
        truck.printRoute()
        print("\n\n")

    UserInput_PkgID = int(input("Please enter package ID number and press enter."))
    print(UserInput_PkgID)
    UserInput_Time = input("Please enter time of day in Miltary time (HH:MM).")
    print(UserInput_Time)
    packagestatuslookup(UserInput_PkgID, UserInput_Time)
