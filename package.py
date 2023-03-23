from typing import Any
import re


class Package:
    def __init__(self, id, address, deadline, notes, status):
      self.id = id
      self.address = address
      self.deadline = int(deadline)
      self.deliveredWithReq = None
      self.delayedReq = False
      self.truckReq = None
      self.wrongAddress = False
      self.status = status
      self.notes = notes
      self.deliverytime = 0
      self.setRequirements(notes)
      self.onTruck = ""

    def setRequirements(self, notes):
        deliveredWith = re.compile(r'Must be delivered with .*')
        truck = re.compile(r'Can only be on truck .*')
        wrongaddress = re.compile(r'Wrong address .*')

        if re.search(truck, notes):
            self.truckReq = int(re.sub(r'\D', "", notes))
        elif re.search(deliveredWith, notes):
            temp = re.sub(r'[a-zA-Z]', "", notes).replace(" ", "")
            strings = temp.split(',')
            numbers = [eval(i) for i in strings]
            self.deliveredWithReq = numbers
        elif re.search(wrongaddress, notes):
            self.wrongAddress = True
        elif notes != "":
            self.delayedReq = True

    def __setattr__(self, name: str, value: Any) -> None:
      super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
      return super().__getattribute__(name)

    def metDeliveryTime (self):
        if self.deliverytime > self.deadline:
            print(self.id, "did not meet deadline of", self.deadline, "delivery time:", self.deliverytime)


