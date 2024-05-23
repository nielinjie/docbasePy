from multiprocessing.managers import BaseManager
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from indexer import createIndex, getIndexState, query




if __name__ == "__main__":
    # init the global index
    print("initializing index...")
    createIndex()

    # setup server
    # NOTE: you might want to handle the password in a less hardcoded way
    manager = BaseManager(("", 5602), b"password")
    manager.register("query", query)
    manager.register("get_index_state",getIndexState)
    server = manager.get_server()

    print("server started...")
    server.serve_forever()
