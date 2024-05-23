import hashlib
import os
from typing import List

from llama_index.core import Document
from llama_index.core import SimpleDirectoryReader


from docbase.infos import FileDocInfo
from docbase.state import DocState, SourceState, findFileDoc


def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield file


def hash_file_string(file):
    return hashlib.md5(file.encode()).hexdigest()


class FileSource:
    state: SourceState
    fileDocs: List[DocState] = []

    def __init__(self, path, name: str):
        self.path = path
        self.name = name

    def readAll(self) -> List[Document]:
        reader = SimpleDirectoryReader(self.path)
        re: List[Document] = []
        for docs in reader.iter_data():
            re.extend(docs)
            for doc in docs:
                print(doc.id_+"...added")
                self.fileDocs.append(DocState(
                    FileDocInfo(
                        path=doc.metadata["file_path"],
                        name=doc.metadata["file_name"],
                        hash=hash_file_string(doc.metadata["file_path"]),
                    ),
                    doc.id_,
                ))
        self.state = SourceState(path=self.path, docs=self.fileDocs)
        return re
    def update(self) :
        nowFiles = self.scan()
        for file in nowFiles:
            savedFile = findFileDoc(self.state, file.path, None)
            if savedFile is None:
                pass 
            else:
                if savedFile.fileDoc.hash != file.hash:
                    pass
                else:
                    pass
    def fileDocId(self, file: str) -> str:
        return self.name + ":" + file

    def scan(self) -> List[FileDocInfo]:
        result = []
        for file in list_files(self.path):
            result.append(
                FileDocInfo(
                    path=os.path.join(self.path, file),
                    name=os.path.basename(file),
                    hash=hash_file_string(file),
                )
            )
        return result
