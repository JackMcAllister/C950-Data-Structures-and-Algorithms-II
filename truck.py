from operator import attrgetter
class Truck:

    def __init__(self, id, packageList, departureTime=0, EODTime=None):
        self.id = id
        self.packageList = packageList
        self.route = []
        self.departureTime = departureTime
        self.EODTime = EODTime
        self.totalDistance = 0

    def getDeliveryTime(self, package_id):
        pass

    @staticmethod
    def checkDistance(double_dict, add1, add2):
        d1 = double_dict.get(add1)
        a = d1.get(add2)
        d2 = double_dict.get(add2)
        b = d2.get(add1)
        if a is not None:
            return a
        elif b is not None:
            return b
        else:
            return None
    @staticmethod
    def distance_to_time(distance):
        minutes = int(float(distance) * (10/3.0))

        return minutes
    @staticmethod
    def convert_time(add_time):
        hours = (add_time // 60) * 100
        minutes = add_time % 60
        return hours + minutes
    # Traveling Salesman sorts my truckLoads into routes and find times of delivery
    def findRoute(self, distance_table):
        deadlineList = []
        EODList = []
        idlist = []
        # assigns truck id to package 'on truck' attribute
        print("Loading packages to truck", self.id, "...")
        for package in self.packageList:
            package.onTruck = self.id
            idlist.append(package.id)
        print(sorted(idlist))

        for package in self.packageList: # puts all EOD deadline packages in a list
            if package.deadline != 2400:
                deadlineList.append(package)
            else:
                EODList.append(package)
        # sorts remaining packages in list by earliest deadline times
        deadlineList.sort(key=attrgetter('deadline'))
        # if a package with EOD time has the same address as a deadline time, add to list
        for deadline_package in deadlineList:
            for EOD_package in EODList:
                if EOD_package.address == deadline_package.address:
                    deadlineList.append(EOD_package)
                    EODList.remove(EOD_package)
                else:
                    pass
        # below builds the route and gets my delivery times
        previous_package = deadlineList[0]
        fromNode = "HUB"
        toNode = previous_package.address
        totalDistance = float(self.checkDistance(distance_table, fromNode, toNode))
        previous_package.deliverytime = self.convert_time(self.distance_to_time(totalDistance)) + self.departureTime
        previous_package.status = 'Delivered at: ' + str(previous_package.deliverytime)
        previous_package.onTruck = self.id
        self.route.append(previous_package)
        deadlineList.remove(previous_package)
        while len(deadlineList) > 0:
            nearestNode = None
            shortestDistance = 9000
            for next_package in deadlineList:
                distance = float(self.checkDistance(distance_table, next_package.address, previous_package.address))
                if distance < shortestDistance:
                    shortestDistance = float(self.checkDistance(distance_table, next_package.address, previous_package.address))
                    nearestNode = next_package
            totalDistance += shortestDistance
            nearestNode.deliverytime = self.convert_time(self.distance_to_time(totalDistance)) + self.departureTime
            nearestNode.status = 'Delivered at: ' + str(nearestNode.deliverytime)
            nearestNode.onTruck = self.id
            self.route.append(nearestNode)
            previous_package = nearestNode
            deadlineList.remove(nearestNode)
        finalAddress = ""
        while len(EODList) > 0:
            nearestNode = None
            shortestDistance = 9000
            for next_package in EODList:
                distance = float(self.checkDistance(distance_table, next_package.address, previous_package.address))
                if distance < shortestDistance:
                    shortestDistance = float(self.checkDistance(distance_table, next_package.address, previous_package.address))
                    nearestNode = next_package
            totalDistance += shortestDistance
            nearestNode.deliverytime = self.convert_time(self.distance_to_time(totalDistance)) + self.departureTime
            nearestNode.status = 'Delivered at: ' + str(nearestNode.deliverytime)
            nearestNode.onTruck = self.id
            self.route.append(nearestNode)
            previous_package = nearestNode
            EODList.remove(nearestNode)
            finalAddress = nearestNode.address
        totalDistance += float(self.checkDistance(distance_table, finalAddress, "HUB"))
        self.totalDistance = totalDistance
        self.EODTime = self.convert_time(self.distance_to_time(totalDistance)) + self.departureTime
        return self.route

    def failedDelivery(self):
        for package in self.packageList:
            package.metDeliveryTime()
    def printRoute(self):
        idlist = []
        for i in self.route:
            idlist.append(i.id)
        print("DELIVERY ROUTE:", idlist)
        print("Total Distance:", round(self.totalDistance))
     #   for i in self.route:
      #      print("ID:", i.id, "\tAddress:", i.address, ",", i.city, ",", i.state, ",", i.zipcode,
       #           "\nWeight in Kilos:", i.weight, "Deadline:", i.deadline, "Delivery Time:", i.deliverytime)
