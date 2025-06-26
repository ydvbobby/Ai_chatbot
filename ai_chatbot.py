import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

# Configure Gemini
genai.configure(api_key="AIzaSyDiuwhNBJruLyuiSJMss09DecWZeJOFqy8")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Prompt template
prompt = PromptTemplate(
    input_variables=['chat_history', 'question'],
    template='Previous Conversation:\n{chat_history}\nUser: {question}\nAI:'
)

# Chat function
def run_chain(question):
    chat_history_txt = '\n'.join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    prompt_text = prompt.format(chat_history=chat_history_txt, question=question)
    response = model.generate_content(prompt_text)
    ai_reply = response.text

    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(ai_reply)
    return ai_reply

# Streamlit UI
st.title('🤖 Personal AI Chatbot🤖')
user_input = st.text_input('Ask Anything 😊 ! ')
if user_input:
    ai_response = run_chain(user_input)
    st.write('You: ', user_input)
    st.write('AI: ', ai_response)

st.subheader('📜 Chat History')
for msg in st.session_state.chat_history.messages:
    st.write(f"{msg.type.capitalize()}: {msg.content}")

