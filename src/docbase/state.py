from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from docbase.infos import FileDocInfo


@dataclass_json
@dataclass
class DocState:
    fileDoc: FileDocInfo
    readerId: str


@dataclass_json
@dataclass
class SourceState:
    path: str
    docs: List[DocState]


def saveState(state: SourceState, path: str):
    with open(path, "w") as f:
        f.write(state.to_json(indent=2))  # type: ignore


def loadState(path: str) -> SourceState:
    with open(path, "r") as f:
        return SourceState.from_json(f.read())  # type: ignore


def findFileDoc(
    sourceState: SourceState, path: str, hash: str | None
) -> DocState | None:
    return next(
        (
            x
            for x in sourceState.docs
            if x.fileDoc.path == path and (hash is None or x.fileDoc.hash == hash)
        ),
        None,
    )
