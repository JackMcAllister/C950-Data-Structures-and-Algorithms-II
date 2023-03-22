from typing import Any
import re


class Package:
    def __init__(self, id, address, deadline, notes, status, deliverytime):
      self.id = id
      self.address = address
      self.deadline = deadline
      self.deliveredWithReq = None
      self.delayedReq = False
      self.truckReq = None
      self.status = status
      self.notes = notes
      self.deliverytime = deliverytime
      self.setRequirements(notes)

    def setRequirements(self, notes):
        deliveredWith = re.compile(r'Must be delivered with .*')
        truck = re.compile(r'Can only be on truck .*')

        if re.search(truck, notes):
            self.truckReq = int(re.sub(r'\D', "", notes))
        elif re.search(deliveredWith, notes):
            temp = re.sub(r'[a-zA-Z]', "", notes).replace(" ", "")
            strings = temp.split(',')
            numbers = [eval(i) for i in strings]
            self.deliveredWithReq = numbers
        elif notes != "":
            self.delayedReq = True

    def __setattr__(self, name: str, value: Any) -> None:
      super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
      return super().__getattribute__(name)


