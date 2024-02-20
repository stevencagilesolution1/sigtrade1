import streamlit as st

url_param = st.query_params.to_dict()
uid = url_param.get("uid", "")
if len(uid):
    st.markdown("Welcome<br>" + uid + "<br>Click <a href='http://43.135.26.66:8501/?uid=" + uid + "' target='_self'>here</a> to start", unsafe_allow_html=True)
