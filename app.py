from time import sleep
import streamlit as st
from functions import add_pdf, available_document, add_csv

title = "RAG Uploader"

# Page 기본값 설정
st.set_page_config(page_title=title, layout="wide")
st.session_state["available_document"] = available_document()
st.header(f"🤖 {title}")
st.divider()

st.subheader("🗃️ Data")
with st.form("my-form", clear_on_submit=True, border=False):
    files = st.file_uploader("_", type=["pdf", "csv"], accept_multiple_files=True, label_visibility="collapsed")
    submitted = st.form_submit_button("submit", use_container_width=True)
    field = st.empty()
    if submitted:
        for data in files:
            field.warning(data.name)
            if data.name.endswith('.pdf'):
                add_pdf(data)
            elif data.name.endswith('.csv'):
                add_csv(data)
            field.success(data.name)
            sleep(0.5)
        field.empty()
        st.session_state["available_document"] = available_document()
docs_name = st.multiselect("**사용 가능한 문서**", key="select_document", options=st.session_state["available_document"])
st.divider()