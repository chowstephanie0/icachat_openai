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
    st.subheader("**About Us: Your Trusted Guide to Singaporean Residency**")
    st.subheader("Project Scope:")
    st.write("Providing a platform for navigating the journey to living, studying, and working in Singapore and assisting foreigners who aspire to make Singapore their new home, whether temporarily or permanently")
    st.subheader("Data Source:")
    st.write("https://www.ica.gov.sg/")
    st.subheader("Use cases:")
    st.write("1. Assisting Foreigners in Determining Eligibility for Staying in Singapore")
    st.write("2. Providing the Latest Data and Trend on Singaporean Citizenship and Permanent Residency")

elif page == 'Immigration Statistics':
    st.subheader("Immigration Statistics")
    st.write("Number And Profile Of Singapore Citizens Granted")
    df = pd.read_csv("SCGranted.csv")
    transposed_df = df.set_index('Data Series').transpose()
    st.write(transposed_df)
    '## Data Series'
    cols = st.multiselect('select columns:', transposed_df.columns, default=[], key=1)

    st.line_chart(
        transposed_df,
        y=cols
    )

    st.write("------------------------------------------------------------------------------")
    st.write("Number And Profile Of Permanent Residents Granted")
    dfPR = pd.read_csv("PRGranted.csv")
    transposed_dfPR = dfPR.set_index('Data Series').transpose()
    st.write(transposed_dfPR)
    '## Data Series'
    colsPR = st.multiselect('select columns:', transposed_dfPR.columns, default=[], key=2)

    st.line_chart(
        transposed_dfPR,
        y=colsPR
    )

elif page == 'Methodology':
    st.subheader("Methodology")
    st.image("icachat_diagram.jpg", caption="Methodology Diagram")
    st.write("Process flow representation for implementing the ChatOpenAI model gpt-4o-mini in LangChain:")
    st.subheader("Process Flow for Implementing ChatOpenAI Model in LangChain")
    st.subheader("1. Ingest Data")
    st.write("      * Source: Collect data from arbitrary sources (e.g., ICA website).")
    st.write("      * Method: Use AsyncHtmlLoader to scrape webpages and load text data into the document loader.")
    st.subheader("2. Split into Chunks")
    st.write("      * Action: Split the loaded text into smaller chunks.")
    st.write("      * Tool: Initialize RecursiveCharacterTextSplitter.")
    st.write("      * Process: Pass the documents to the splitter to create manageable text pieces.")
    st.subheader("3. Create Embeddings")
    st.write("    * Action: Convert the text chunks into numerical values (embeddings).")
    st.write("    * Purpose: Represent the semantic meaning of the text for quick retrieval.")
    st.write("    * Method: Use text-embedding-3-large model to create embeddings for each chunk.")
    st.subheader("4. Load Embeddings into Vector Store")
    st.write("    * Action: Store the generated embeddings in a vector store.")
    st.write("    * Type: Use FAISS for effective similarity search.")
    st.write("    * Benefit: Vector stores optimize the retrieval of similar documents compared to traditional databases.")
    st.subheader("5. Query Data")
    st.write("    * Action: Search for relevant information in the vector store using embeddings.")
    st.write("    * Tool: Initialize ConversationalRetrievalChain.")
    st.write("    * Functionality: Allows the chatbot to have memory and rely on the vector store for retrieving relevant information.")
    st.write("    * Optional: Set return_source_documents=True to include source documents in responses.")
    st.subheader("6. Generate Answer")
    st.write("    * Action: Pass the users question along with the relevant information.")
    st.write("    * Process: Use the question-answering chain (powered by the language model) to generate a response based on the query and the retrieved information.")

    st.subheader("Summary Flow")
    st.write("1. Ingest Data → 2. Split into Chunks → 3. Create Embeddings → 4. Load into Vector Store → 5. Query Data → 6. Generate Answer")
    st.write("This structured flow outlines the steps needed to implement the ChatOpenAI model within the LangChain framework, ensuring clarity and systematic execution of tasks.")
