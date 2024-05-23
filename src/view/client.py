from multiprocessing.managers import BaseManager
from typing import Any

class Client:
    def __init__(self):
        self.manager = BaseManager(("", 5602), b"password")
        self.manager.register("query")
        self.manager.register("get_index_state")
        self.manager.connect()

    def query(self, text:str) -> Any:
        return self.manager.query(text)._getvalue() # type: ignore

    def get_index_state(self):
        return self.manager.get_index_state()._getvalue() # type: ignore



