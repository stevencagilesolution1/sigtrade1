import streamlit as st

url_param = st.query_params.to_dict()
st.write(url_param)
