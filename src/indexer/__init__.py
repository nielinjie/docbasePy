import multiprocessing
import os
from typing import Any
from llama_index.core import load_index_from_storage
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from indexer.preparing import Done, NeedPrepare, NotStarted, Preparing
from llama_index.core import Settings

from view import IndexState, NotReady, ResultState, StateView


from dotenv import load_dotenv
load_dotenv()


indexInstance: NeedPrepare = NotStarted()
embeddingModel = None
lock = multiprocessing.Lock()

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base=os.getenv("LLM_API_BASE"),
    api_key= os.getenv("LLM_API_KEY"),
)


def getIndexState() -> StateView:
    global indexInstance
    with lock:
        if isinstance(indexInstance, NotStarted):
            return NotReady("starting")
        if isinstance(indexInstance, Preparing):
            return NotReady("preparing")
        if isinstance(indexInstance, Done):
            return IndexState(indexInstance.result)  # type: ignore
        return NotReady("error")

def query(text:str) -> StateView:
    global indexInstance
    if text == "":
        return NotReady("(no query string inputted)")
    if isinstance(indexInstance, Done):
        index = indexInstance.result
        return ResultState(index.as_query_engine().query(text))
    return NotReady("(no index find)")

def getIndexInstance() -> NeedPrepare:
    global indexInstance
    return indexInstance

def createIndex():
    global indexInstance
    with lock:
        indexInstance = Preparing()
        print("change to prepared")
    print("creating index")
    index = loadIndex()
    print("done creating")
    with lock:
        indexInstance = Done(index)
        print("change to done!!")


def loadIndex():
    global embeddingModel
    path = "./indexStore"
    embeddingModel = HuggingFaceEmbedding(
        model_name="BAAI/bge-large-zh-v1.5",
    )
    sc = StorageContext.from_defaults(persist_dir=path)
    index = load_index_from_storage(sc, None, embed_model=embeddingModel)
    return index


# def index():
#     embeddingModel = HuggingFaceEmbedding(
#         model_name="BAAI/bge-large-zh-v1.5",
#     )
#     # embed_model = OpenAIEmbedding(
#     #     api_base="xxx",
#     #     api_key="xxxxx",
#     # )

#     path = "/Users/nielinjie/Projects/DocBaseData/small"
#     fileSource = FileSource(path, "fileSource - " + path)
#     docs = fileSource.readAll()
#     iS = SimpleIndexStore()  # .from_persist_path("./indexStore")
#     sc = StorageContext.from_defaults(index_store=iS)
#     index = VectorStoreIndex.from_documents(
#         docs, storage_context=sc, embed_model=embeddingModel
#     )
#     index.storage_context.persist("./indexStore")
