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
    st.text("da nhan cau hoi")

    llm = OllamaLLM(model='llama3.2')
    st.text("da co model")
    prompt = PromptTemplate.from_template(template=template)
    st.text("da co template")
        
    chain = prompt | llm | StrOutputParser()
    st.text("da co chain")
    rag_context = ''
        
    context = f"Với các thông tin sau (nếu có):\n{rag_context}\nHãy trả lời câu hỏi:\n"
    st.text("da co context")
    st.text(f"{chat_history}")
    respones = chain.invoke({"question": context + user_query, "history": chat_history})
    st.text(respones)
    
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
st.text("da hoi")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    st.text("da in cau hoi")
    with st.chat_message("AI"):
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    st.text("da dua ra cau tra loi")

    st.session_state.chat_history.append(AIMessage(content=response))
    st.text("da luu cau tra loi")