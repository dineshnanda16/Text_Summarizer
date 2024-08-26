import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.llms import Cohere
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(page_title="Text Summarizer", page_icon=":memo:")
st.title("Text Summarizer")

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get summary
def get_summary(text):
    template = "Please summarize the following text:\n\nText: {user_text}"
    prompt = ChatPromptTemplate.from_template(template)
    llm = Cohere(cohere_api_key="YOUR_COHERE_API_KEY")
    chain = LLMChain(prompt=prompt, llm=llm)
    return chain.run({"user_text": text})

# Display chat history
for message in st.session_state.chat_history:
    role = "AI" if isinstance(message, AIMessage) else "Human"
    with st.chat_message(role):
        st.write(message.content)

# User input
user_input = st.text_area("Enter text to summarize here...", height=150)

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.chat_message("Human").markdown(user_input)
    
    summary = get_summary(user_input)
    st.chat_message("AI").write(summary)
    
    st.session_state.chat_history.append(AIMessage(content=summary))
