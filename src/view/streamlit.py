import os
import sys
import streamlit as st


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from view.client import Client


@st.cache_resource
def get_client():
    return Client()


st.markdown("# Query from Documents")
st.markdown("## Index State")
doing = st.empty()
get_client().get_index_state().render(doing)
st.markdown("## Query:")
st.text_input("Query", key="query")
st.markdown("## Result:")
result = st.empty()
get_client().query(st.session_state.query).render(result)
