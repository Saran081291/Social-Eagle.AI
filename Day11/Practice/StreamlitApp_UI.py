import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

# 1. Load environment variables
load_dotenv()

# 2. Page Configuration
st.set_page_config(page_title="GenAI Chatbot", page_icon="🤖")
st.title("🤖 My First GenAI Chatbot")

# 3. Setup Streamlit Chat History (Session State Memory)
# This automatically stores conversation history in Streamlit's session memory
history = StreamlitChatMessageHistory(key="chat_messages")

# 4. Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 5. Create Prompt with Memory Placeholder
# ChatPromptTemplate supports system instructions, message history, and user input
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly and helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),  # Inject past message history here
    ("human", "{input}")
])

# 6. Build the Chain with Memory capabilities
chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history",
)

# 7. Display past chat messages on app reload
for msg in history.messages:
    # Match LangChain message types to Streamlit chat interface roles
    role = "user" if msg.type == "human" else "assistant"
    st.chat_message(role).write(msg.content)

# 8. Handle User Input from Streamlit Chat UI
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display user's message immediately
    st.chat_message("user").write(user_input)

    # Generate and display assistant's response
    with st.chat_message("assistant"):
        response = chain_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "default_session"}}
        )
        st.write(response.content)