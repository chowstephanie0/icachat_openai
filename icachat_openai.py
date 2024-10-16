from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from torch import cuda, bfloat16
import transformers
import torch
import streamlit as st
import time
from streamlit_chat import message
import getpass
import os

#if not os.getenv("OPENAI_API_KEY"):
os.environ["OPENAI_API_KEY"] = "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"

DB_FAISS_PATH = 'vectorstore/db_faiss'

urls =["https://www.ica.gov.sg/reside/citizenship/apply", "https://www.ica.gov.sg/reside/PR/apply","https://www.ica.gov.sg/reside/LTVP/apply","https://www.ica.gov.sg/reside/STP/apply","https://www.ica.gov.sg/reside/pre-marriage-long-term-visit-pass-assessment","https://www.ica.gov.sg/reside/citizenship/minor-oath-taking", "https://www.ica.gov.sg/reside/citizenship/roe","https://www.ica.gov.sg/reside/citizenship/confirmation","https://www.ica.gov.sg/reside/PR/apply-REP","https://www.ica.gov.sg/reside/PR/transfer-REP","https://www.ica.gov.sg/reside/STP/sponsor"]
loader = AsyncHtmlLoader(urls)
docs = loader.load()

#print(docs)

html2text = Html2TextTransformer()
docs_transformed = html2text.transform_documents(docs)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs_transformed)


llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

db = FAISS.from_documents(texts, embeddings)
db.save_local(DB_FAISS_PATH)


def conversational_chat(query):
    QUESTION_PROMPT = PromptTemplate.from_template("""
        Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.
        This is a conversation with a human. Answer the questions you get based on the knowledge you have.
        You are a very proficient Singapore Immigration Officer that speaks and writes immigration documents proficiently.
        """)
    print('Sending completion call to OpenAI...')
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(search_type="similarity", search_kwargs={'k':3}), return_source_documents=True, condense_questio
n_prompt=QUESTION_PROMPT, verbose=True)
   
    chat_history = []

    result = chain.invoke({"question": query, "chat_history": chat_history})
    for word in result["answer"].split():
        yield word + " "
        time.sleep(0.05)