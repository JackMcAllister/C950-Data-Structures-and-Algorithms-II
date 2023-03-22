from typing import Any

# under 16 pcks
#still working on this
class Truck:

    def __init__(self, id, packageList, departureTime=None, EODTime=None ):
        self.id = id
        self.packageList = packageList
        self.route = []
        self.departureTime = departureTime
        self.EODTime = EODTime
    def getDeliveryTime(self, package_id):
        pass

    def findRoute(self, distance_table):  # greedy algo sorts my truckLoads into routes and find times of delivery
        route = None
        # prioritize early delivery times, 2 trucks traveling at time (2 drivers)
        # go to the next closest address
        # leaves hub at 8:00 unless a package is arriving late in trucks list
        # check in truck needs to go to hub (if all packages are empty then driver switches trucks)
        # update any addresses at specified time. wrong address can't be delivered yet
        # when address is updated at time new add given, EOD= back of list otherTime=filed in appropriate spot
        # when packages is delivered add distance to totalDistanceDriven variable

        self.route = route






