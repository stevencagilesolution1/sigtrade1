import streamlit as st

url_param = st.query_params.to_dict()
code = url_param.get("code", "")
scope = url_param.get("scope", "")
authuser = url_param.get("authuser", "")
prompt = url_param.get("prompt", "")
st.write(url_param)

if len(url_param):
  st.markdown("<a href='http://43.135.26.66:8501/?code=" + code + "&scope=" + scope + "&authuser=" + authuser + "&prompt=" + prompt + "' target='_self'>GO</a>", unsafe_allow_html=True)
