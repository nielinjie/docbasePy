from abc import ABC, abstractmethod
from pydoc import doc
from typing import Any
import streamlit as st

from attr import dataclass
from llama_index.core import VectorStoreIndex


class StateView(ABC):
    @abstractmethod
    def render(self, widget):
        pass


@dataclass
class NotReady(StateView):
    info: str | None

    def render(self, widget):
        with widget.expander("🟠 Not Ready."):
            st.markdown(
                "Not ready: " + (self.info or "(no info)"),
            )


class IndexState(StateView):
    indexId: str
    docsCount: int
    files: list[str]

    def __init__(self, index: VectorStoreIndex):
        self.indexId = index.index_id
        self.docsCount = len(index.docstore.docs)
        self.files = list(set(x.metadata["file_path"] for x in index.docstore.get_all_ref_doc_info().values()))  # type: ignore

    def render(self, widget):
        with widget.expander(" 🟢 Index is Ready"):
            st.markdown(
                "Files in index: \n\n" + "\n".join("- " + item for item in self.files),
            )

class ResultState(StateView):
    text:str
    sourceNodes:Any
    def __init__(self,response) -> None:
        self.text = response.response
        self.sourceNodes = response.source_nodes
    def render(self, widget):
        with widget.container() :
            st.markdown(self.text)
            with st.expander("more infos...") :
                st.write(self.sourceNodes)