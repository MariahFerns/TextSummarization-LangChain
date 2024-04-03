# Installing required libraries
# !pip install -r requirements.txt

# Importing required libraries
import streamlit as st
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

def generate_response(txt):
    # 1. Instantiate the LLM model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    
    
    # 2. Split the input text using textsplitter
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)    
    
    
    # 3. Create multiple documents for the splitted text
    docs = [Document(page_content=t)  for t in texts]
    
    
    # 4. Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)
    
# Building the streamlit web interface

# Set Title
st.set_page_config(page_title='Text Summarization App')
st.title('Text Summarization App')

# Take input text
txt_input = st.text_area('Enter your text', '', height=200)

# Form to accept user API key and generate result
result=[]
with st.form('summarize_form', clear_on_submit=True): # Clears Open API key entered after submitting (for security) 
    openai_api_key = st.text_input('Open AI API Key', type='password')
    submitted = st.form_submit_button('Submit')
    # Checking if user has entered api key and clicked on submit
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(txt_input)
            result.append(response)
            del openai_api_key # deleting the key for security 

# Printing the output
if len(result):
    st.info(response)
    