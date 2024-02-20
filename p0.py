import pandas
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import mysql.connector
import yfinance
import numpy
from google_auth import get_logged_in_user_email, show_login_button

host = "43.135.26.66"
# host = "localhost"
st.set_page_config(page_title="SigTrade", page_icon="large_purple_circle", layout="wide", initial_sidebar_state="collapsed")
style = """
<style>
  [data-testid="collapsedControl"] {display: none;}
  .stDeployButton {display:none;}
  header {visibility: hidden;}
  @import url("https://fonts.googleapis.com/css2?family=Lato:wght@300;400&display=swap");
  @font-face {font-family: "Lato", sans-serif; color: white;}
  html, body, [class*="css"]  {font-family: "Lato"; font-size: 6px;}
  #rcorners {border-radius: 15px 50px 30px 5px; background: #FFFFFF; padding: 6px; width: 100px; height: 100px; border:0;}
  #rcornersb {border-radius: 15px 50px 30px 5px; padding: 6px; width: 100px; height: 100px; border:0;}
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  a:link {text-decoration: none;}
  a:visited {text-decoration: none;}
  a:hover {text-decoration: none;}
  a:active {text-decoration: none;}
  .divTable {display: table; width: 100%;}
  .divTablePurple {border: 0; display: table; width: 100%; border-radius: 15px 15px 15px 15px; background: #3E0149; padding: 5px; padding-top: 15px;}
  .divTableRow {border: 0; display: table-row;}
  .divTableCell {border: 0; display: table-cell; padding: 2px; color: #3E0149;}
  .divTableCell1 {vertical-align: top; border: 0; display: table-cell; padding: 2px; color: #3E0149; width: 10%;}
  .divTableCell2 {vertical-align: top; border: 0; display: table-cell; padding: 2px; color: #3E0149; width: 50%;}
  .divTableCell3 {vertical-align: top; border: 0; display: table-cell; padding: 2px; color: #3E0149; width: 20%;}
  .divTableCell4 {vertical-align: top; border: 0; display: table-cell; padding: 2px; color: #3E0149; width: 20%;}
  .divTableBody {border: 0; display: table-row-group;}
  .divTableBodyPad {border: 0; display: table-row-group; padding: 5px;}
  .divButtonStrat {border: 0; display: table-cell; padding: 5px; border-radius: 25px 15px 15px 25px; background: #D9D9D9;}
  .divButtonInfo {border: 0; display: table-cell; padding: 3px; border-radius: 5px 5px 5px 5px; background: #6E3F77; margin: 3px;}
  .divButtonInfoBlank {border: 0; display: table-cell; width: 40px;}
  .divBlankHeight {height: 2px;}
</style>
"""
url_param = st.query_params.to_dict()
mode = url_param.get("mode", "login")
st.markdown(style, unsafe_allow_html=True)
if mode == "login":
    user_email = get_logged_in_user_email()
    if not user_email:
        show_login_button()
        st.session_state.email = ""
    else:
        uid = str(st.session_state.email)
        st.markdown("Welcome<br>" + uid + "<br>Click <a href='http://43.135.26.66:8501/?uid=" + uid + "' target='_self'>here</a> to start", unsafe_allow_html=True)
elif mode == "usercenter":
    st.markdown("<font size='7'>User center</font>", unsafe_allow_html=True)
