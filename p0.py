import streamlit as st

url_param = st.query_params.to_dict()
code = url_param.get("code", "U0000001")
scope = url_param.get("scope", "U0000001")
authuser = url_param.get("authuser", "U0000001")
prompt = url_param.get("prompt", "U0000001")
st.write(url_param)

if len(url_param):
  st.markdown("<a href='http://43.135.26.66:8501/?code=" + code + "&scope=" + scope + "&authuser=" + authuser + "&prompt=" + prompt + "' target='_self'>GO</a>", unsafe_allow_html=True)
