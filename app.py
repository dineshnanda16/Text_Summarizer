import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.llms import Cohere
from langchain.chains import LLMChain

# Define message classes
class HumanMessage:
    def __init__(self, content):
        self.content = content

class AIMessage:
    def __init__(self, content):
        self.content = content

# Ensure session state is initialized
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="Text Summarizer", page_icon=":memo:")
st.title("Text Trim")

def get_summary(text, length="short", tone="neutral"):
    template = """
    Please summarize the following text with a {length} length and a {tone} tone:

    Text: {user_text}

    Also, extract keywords and analyze the sentiment of the text.
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = Cohere(cohere_api_key="r6H0r9mAApORRZgBIUJqgMT4I3EwYYpZtqOtyEKI")

    chain = LLMChain(prompt=prompt, llm=llm)

    return chain.run({"user_text": text, "length": length, "tone": tone})

def extract_keywords(text):
    # Placeholder implementation for keyword extraction
    return ["keyword1", "keyword2", "keyword3"]

def analyze_sentiment(text):
    # Placeholder implementation for sentiment analysis
    return "Positive"  # or "Negative", "Neutral"

# Sidebar options
st.sidebar.header("Customize your summary")
length_option = st.sidebar.radio("Select summary length:", ("short", "medium", "long"))
tone_option = st.sidebar.radio("Select summary tone:", ("neutral", "formal", "informal"))

user_input = st.chat_input("Enter text to summarize here...")

if user_input:
    # Append the human message to the chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Generate the summary
    summary = get_summary(user_input, length=length_option, tone=tone_option)

    # Append the AI summary to the chat history
    st.session_state.chat_history.append(AIMessage(content=summary))

    # Keep only the last 5 entries in the history
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = st.session_state.chat_history[-10:]

# Display the chat history (last 5 interactions)
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# Display extracted keywords and sentiment analysis results for the last message
if st.session_state.chat_history:
    last_user_input = st.session_state.chat_history[-2].content if len(st.session_state.chat_history) > 1 else None
    last_summary = st.session_state.chat_history[-1].content if len(st.session_state.chat_history) > 0 else None

    if last_user_input and last_summary:
        with st.expander("Summary Details"):
            st.write("**Keywords:**", extract_keywords(last_user_input))
            st.write("**Sentiment:**", analyze_sentiment(last_user_input))
