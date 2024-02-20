import jwt
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token
import urllib.parse
import asyncio
from typing import Optional
import webbrowser

client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
redirect_url = st.secrets["redirect_url"]
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


url_param = st.query_params.to_dict()
user_email = get_logged_in_user_email()
st.write("user_email:", user_email)

if len(url_param):
  webbrowser.open_new("http://43.135.26.66:8501/?uid=" + user_email)
  st.link_button("Go to homepage", "http://43.135.26.66:8501/?uid=" + user_email)
  st.markdown("<a href='http://43.135.26.66:8501/?uid=" + user_email + "' target='_top'>GO</a>", unsafe_allow_html=True)
