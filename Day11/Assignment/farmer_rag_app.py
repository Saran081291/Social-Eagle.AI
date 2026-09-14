import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough

# 1. Load Environment Variables (.env)
load_dotenv()

# Streamlit Page Setup
st.set_page_config(
    page_title="Kisan Sahayak - Farmer Welfare Portal",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling
css_style = """
<style>
.stApp {
    background-color: #f7fbf7;
}
.main-header {
    background: linear-gradient(135deg, #1e5631 0%, #4c9a2a 100%);
    padding: 24px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.main-header h1 {
    color: #ffffff !important;
    margin-bottom: 5px;
    font-weight: 700;
}
.main-header p {
    color: #e2f0d9;
    font-size: 1.1rem;
    margin: 0;
}
section[data-testid="stSidebar"] {
    background-color: #eaf4ea;
    border-right: 2px solid #c8e6c9;
}
.stat-card {
    background-color: #ffffff;
    border-left: 5px solid #2e7d32;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.stat-card h4 {
    color: #2e7d32;
    margin: 0 0 4px 0;
}
.stat-card p {
    color: #555555;
    font-size: 0.9rem;
    margin: 0;
}
</style>
"""
st.markdown(css_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=600&q=80", caption="Supporting Farmers Across India 🇮🇳")
    
    st.title("🌱 Quick Navigation")
    
    sidebar_card = """
    <div class="stat-card">
        <h4>🏛️ Key Schemes Covered</h4>
        <p>• <b>PM-KISAN</b> (Income Support)</p>
        <p>• <b>KCC</b> (Subsidized Credit)</p>
        <p>• <b>PMFBY</b> (Crop Insurance)</p>
    </div>
    """
    st.markdown(sidebar_card, unsafe_allow_html=True)

    st.markdown("### 📌 Quick Helpful Queries")
    st.info("💡 Click/Copy any query to ask:")
    st.markdown("1. *What are the PM-Kisan financial benefits?*")
    st.markdown("2. *Who is eligible for Kisan Credit Card (KCC)?*")
    st.markdown("3. *How to claim PM Fasal Bima Yojana crop insurance?*")

    st.divider()
    
    st.markdown("### 🔗 Official Portals")
    st.markdown("[🌾 PM-Kisan Official Portal](https://pmkisan.gov.in)")
    st.markdown("[💳 Kisan Credit Card Info](https://pmkisan.gov.in)")
    st.markdown("[🛡️ PM Fasal Bima Portal](https://pmfby.gov.in)")

# Header
header_html = """
<div class="main-header">
    <h1>🌾 Kisan Sahayak - AI Agriculture Assistant</h1>
    <p>Get instant answers on Government Farmer Schemes, Subsidies & Financial Support</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Verify API Key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY is missing! Please configure your .env file.")
    st.stop()

# Vector Store Setup
@st.cache_resource
def initialize_vector_store():
    file_path = os.path.join("..", "Notes", "scraped_farmer_schemes.txt")
    
    if not os.path.exists(file_path):
        st.error(f"⚠️ File not found at '{file_path}'. Please run scraper.py first.")
        st.stop()

    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

with st.spinner("🌾 Loading Government Schemes Knowledge Base..."):
    vectorstore = initialize_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Guardrails
def input_guardrail(user_query: str) -> bool:
    allowed_keywords = [
        "farmer", "kisan", "scheme", "pm-kisan", "crop", "subsidy", "insurance", 
        "land", "money", "benefit", "eligibility", "register", "apply", "loan", 
        "kcc", "fasal", "bima", "government", "aadhaar", "bank", "help"
    ]
    query_lower = user_query.lower()
    return any(keyword in query_lower for keyword in allowed_keywords)

def output_guardrail(response_text: str) -> str:
    if not response_text or not response_text.strip():
        return "I apologize, but I could not find relevant scheme details in official records."
    return response_text

# Memory and Chain Setup
history = StreamlitChatMessageHistory(key="farmer_chat_history")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are 'Kisan Sahayak', an empathetic and knowledgeable AI assistant guiding Indian farmers on official government welfare schemes and financial benefits.
    
    Rules:
    1. Answer strictly using the provided context from official government records.
    2. Format key points using bullet points and clear bold headings.
    3. Keep language simple, respectful, and easy to understand for farmers.
    4. If details are missing, politely inform that official scheme records do not contain the answer.

    Retrieved Context:
    {context}"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

base_chain = (
    RunnablePassthrough.assign(
        context=lambda x: format_docs(retriever.invoke(x["question"]))
    )
    | prompt_template
    | llm
    | StrOutputParser()
)

rag_chain = RunnableWithMessageHistory(
    runnable=base_chain,
    get_session_history=lambda session_id: history,
    input_messages_key="question",
    history_messages_key="history"
)

# Chat Interface
for msg in history.messages:
    avatar = "👨‍🌾" if msg.type == "human" else "🌾"
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(name=role, avatar=avatar):
        st.write(msg.content)

user_input = st.chat_input("Ask about PM-Kisan, KCC, Fasal Bima Yojana, eligibility, etc...")

if user_input:
    with st.chat_message(name="user", avatar="👨‍🌾"):
        st.write(user_input)

    if not input_guardrail(user_input):
        warning_msg = "🚨 **Guardrail Alert**: This portal is strictly dedicated to Farmer Benefits and Government Agricultural Schemes. Please ask a relevant query."
        with st.chat_message(name="assistant", avatar="🌾"):
            st.error(warning_msg)
    else:
        with st.chat_message(name="assistant", avatar="🌾"):
            with st.spinner("Searching official government portal records..."):
                raw_response = rag_chain.invoke(
                    {"question": user_input},
                    config={"configurable": {"session_id": "farmer_session"}}
                )
                final_response = output_guardrail(raw_response)
                st.write(final_response)