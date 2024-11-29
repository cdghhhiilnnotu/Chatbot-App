import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# app config
st.set_page_config(page_title="Streaming bot", page_icon="🤖")
st.title("Streaming bot")

def get_response(user_query, chat_history):

    template = """
    Tên của bạn là AIMAGE
    Đây là lịch sử trò chuyện: {history}

    {question}
    Trả lời:
    """

    llm = OllamaLLM(model='llama3.2')
    
    prompt = PromptTemplate.from_template(template=template)
        
    chain = prompt | llm | StrOutputParser()
    rag_context = ''
        
    context = f"Với các thông tin sau (nếu có):\n{rag_context}\nHãy trả lời câu hỏi:\n"
    
    return chain.stream({"question": context + user_query, "history": chat_history})

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))