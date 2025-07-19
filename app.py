import streamlit as st
import os
from dotenv import load_dotenv
import mysql.connector
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter

# Load environment variables
load_dotenv()

# Database connection
@st.cache_resource
def init_database():
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    connection_string = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    db = SQLDatabase.from_uri(connection_string)
    return db

# Initialize LLM and chain
@st.cache_resource
def init_chain():
    db = init_database()
    llm = OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY'))
    
    # Create SQL query chain
    generate_query = create_sql_query_chain(llm, db)
    execute_query = QuerySQLDataBaseTool(db=db)
    
    # Answer prompt
    answer_prompt = PromptTemplate.from_template(
        """Based on the question, SQL query, and result, provide a clear answer:

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
    )
    
    # Complete chain
    chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer_prompt
        | llm
    )
    
    return chain

# Streamlit app
st.title("Database Q&A Assistant")
st.write("Ask questions about your database:")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your question:"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response
    try:
        chain = init_chain()
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                response = chain.invoke({"question": prompt})
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        with st.chat_message("assistant"):
            st.error(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
