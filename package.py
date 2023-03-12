from typing import Any


class Package:
    def __init__(self, id, address, deadline, notes, status, deliverytime):
      self.id = id
      self.address = address
      self.deadline = deadline
      self.notes = notes
      self.status = status
      self.deliverytime = deliverytime

    def __setattr__(self, name: str, value: Any) -> None:
      super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
      return super().__getattribute__(name)


