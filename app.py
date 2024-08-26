import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.llms import Cohere
from langchain.chains import LLMChain

class HumanMessage:
    def __init__(self, content):
        self.content = content

class AIMessage:
    def __init__(self, content):
        self.content = content


load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Text Summarizer", page_icon=":memo:")
st.title("Text Summarizer")

def get_summary(text):
    template = """
    Please summarize the following text:

    Text: {user_text}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = Cohere(cohere_api_key="r6H0r9mAApORRZgBIUJqgMT4I3EwYYpZtqOtyEKI")

    chain = LLMChain(prompt=prompt, llm=llm)

    return chain.run({"user_text": text})

# Initialize chat history with a default message
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Please enter the text you would like to summarize.")
    ]

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

user_input = st.chat_input("Enter text to summarize here...")
if user_input is not None and user_input != "":
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("Human"):
        st.markdown(user_input)

    with st.chat_message("AI"):
        summary = get_summary(user_input)
        st.write(summary)

    st.session_state.chat_history.append(AIMessage(content=summary))
