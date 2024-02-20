import pandas
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import mysql.connector
import asyncio
from typing import Optional
import jwt
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token
import urllib.parse

client_id = "620631027700-hroqcepujs3dki4duhfa3acn99gkujrn.apps.googleusercontent.com"
client_secret = "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"
redirect_url = "https://sigtrade.store/"
client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)

def decode_user(token: str):
    """
    :param token: jwt token
    :return:
    """
    decoded_data = jwt.decode(jwt=token, options={"verify_signature": False})
    return decoded_data

async def get_authorization_url(client: GoogleOAuth2, redirect_url: str) -> str:
    authorization_url = await client.get_authorization_url(redirect_url, scope=["email"], extras_params={"access_type": "offline"})
    return authorization_url

def markdown_button(url: str):
    st.markdown(
        f"""
        <center>
        <a href="{url}" target="_self">
        <br><br><br><br><br><br><br><br>
        <div style="
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            font-size: 15px;
            padding: 0.25rem 0.75rem;
            border-radius: 0.5rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: #DD4B39;
            color: rgb(255, 255, 255);
            text-decoration: none;
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); padding: 10px;
            ">
            Login with Google&nbsp;
            <img src="https://live.staticflickr.com/65535/53532609140_14bc15693f_o.png" width="40" height="40">
        </div>
        </a>
        </center>
    """, unsafe_allow_html=True)

async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str) -> OAuth2Token:
    token = await client.get_access_token(code, redirect_url)
    return token

def get_access_token_from_query_params(client: GoogleOAuth2, redirect_url: str) -> OAuth2Token:
    query_params = st.query_params.to_dict()
    code = urllib.parse.quote(query_params["code"])
    token = asyncio.run(get_access_token(client=client, redirect_url=redirect_url, code=code))
    st.query_params.clear()
    return token

def show_login_button():
    authorization_url = asyncio.run(get_authorization_url(client=client, redirect_url=redirect_url))
    markdown_button(authorization_url)

def get_logged_in_user_email() -> Optional[str]:
    if "email" in st.session_state:
        return st.session_state.email
    try:
        token_from_params = get_access_token_from_query_params(client, redirect_url)
    except KeyError:
        return None
    user_info = decode_user(token=token_from_params["id_token"])
    st.session_state["email"] = user_info["email"]
    return user_info["email"]


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
