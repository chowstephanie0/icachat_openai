import streamlit as st
import time
import random
import hmac
import pandas as pd
from utility import check_password
from icachat_openai import conversational_chat

# region <--------- Streamlit Page Configuration --------->

st.set_page_config(
    layout="centered",
    page_title="ICA Chat App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit Page Configuration --------->

st.sidebar.title("Main")

page = st.sidebar.radio("Go To",["ICA Immigration Eligibility", "About Us", "Immigration Statistics", "Methodology"])

if page == 'ICA Immigration Eligibility':

  st.markdown("<h1 style='text-align: center;'>ICA.CHAT</h1>", 
              unsafe_allow_html=True)

  st.markdown("<h3 style='text-align: center;'>Your Virtual Web Companion!</h3>", 
              unsafe_allow_html=True)

  st.write("Meet I.C.A.CHAT: Your interactive browsing companion. Query your eligibility to Reside, Study and Work in Singapore using AI.")
  st.write("Eg. I am 18 years old. How can I be eligible to be a Singapore Permanent Resident?")
  st.write("Eg. I am married to a Singaporean. How can I be eligible to be a Singapore Permanent Resident?")

  # Initialize chat history
  if "messages" not in st.session_state:
      st.session_state.messages = []

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
         st.markdown(message["content"])

  # Accept user input
  if prompt := st.chat_input("Hi, how can I help you?"):
     # Add user message to chat history
     st.session_state.messages.append({"role": "user", "content": prompt})
     # Display user message in chat message container
     with st.chat_message("user"):
          st.markdown(prompt)

     # Display assistant response in chat message container
     with st.chat_message("assistant"):
          response = st.write_stream(conversational_chat(prompt))
          # Add assistant response to chat history
     st.session_state.messages.append({"role": "assistant", "content": response})

elif page == 'About Us':
    st.subheader("Welcome to About Us")

elif page == 'Immigration Statistics':
    st.subheader("Immigration Statistics")
    df = pd.read_csv("SCGranted.csv")
    transposed_df = df.set_index('Data Series').transpose()
    st.write(transposed_df)
    '## Data Series'
    cols = st.multiselect('select columns:', transposed_df.columns, default=[])

    st.line_chart(
        transposed_df,
        y=cols
    )

elif page == 'Methodology':
    st.subheader("Methodology")