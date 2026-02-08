import streamlit as st
import requests 
BASE_URL="http://127.0.0.1:8000"
st.set_page_config(page_title="Intelligent Cache Eviction", layout="wide")
st.title("Intelligent API Cache Eviction Dashboard")
url=st.text_input(
    "Enter API URL",
    "https://jsonplaceholder.typicode.com/posts/1"
)
col1,col2=st.columns(2)
if col1.button("Smart Cache"):
    try:
        response=requests.post(
            f"{BASE_URL}/request-smart",
            json={"url":url}
        )
        data=response.json()
        st.success("Request Success")
        st.write("### Result")
        st.json(data)
    except Exception as e:
        st.error(str(e))
if col2.button("Normal LRU Cach"):
    try:
        response=requests.post(
            f"{BASE_URL}/request-normal",
            json={"url":url}
        )
        data=response.json()
        st.success("Request Success")
        st.write("### Result")
        st.json(data)
    except Exception as e:
        st.error(str(e))
st.divider()
if st.button("Smart Cache Eviction Log"):
    try:
        response=requests.get(f"{BASE_URL}/intelligent-evictions")
        data=response.json()
        st.subheader("Intelligent Cache Eviction Log")
        st.json(data)
    except Exception as e:
        st.error(str(e))
st.divider()
if st.button("Normal LRU Eviction Log"):
    try:
        response=requests.get(f"{BASE_URL}/normal-evictions")
        data=response.json()
        st.subheader("Normal LRU Eviction Log")
        st.json(data)
    except Exception as e:
        st.error(str(e))
st.divider()
if st.button("Compare Both"):
    try:
        response=requests.get(f"{BASE_URL}/comparison")
        data=response.json()
        st.subheader("Comparison Result")
        st.json(data)
    except Exception as e:
        st.error(str(e))