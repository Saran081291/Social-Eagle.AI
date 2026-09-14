import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load API Key
load_dotenv()

# 2. Page Configuration
st.set_page_config(page_title="RAG Document Q&A", page_icon="📚")
st.title("📚 Chat with your Documents (RAG)")

# Initialize session state for vectorstore if not existing
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# --- SIDEBAR: File Upload & Processing ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing file..."):
            # Save uploaded file temporarily to disk
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name

            # Load document content based on extension
            if file_extension == ".pdf":
                loader = PyPDFLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path)

            docs = loader.load()

            # Split text into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            splits = text_splitter.split_documents(docs)

            # Generate Embeddings and create FAISS Vector Store
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(splits, embeddings)

            # Save in Streamlit Session State
            st.session_state.vectorstore = vectorstore
            st.success(f"Document processed successfully! Created {len(splits)} text chunks.")

            # Clean up temporary file
            os.remove(tmp_path)

# --- MAIN CHAT INTERFACE ---
st.header("2. Ask Questions About Your Document")

if st.session_state.vectorstore is None:
    st.info("👈 Please upload and process a document in the sidebar to get started.")
else:
    # 3. Setup RAG Chain
    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Prompt instructing LLM to answer using ONLY retrieved context
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know based on the document.

    Context:
    {context}

    Question: {question}

    Answer:
    """)

    # Helper function to format retrieved documents into a single text block
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # LCEL RAG Chain Definition
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Question Input
    user_query = st.chat_input("Ask something about your document...")

    if user_query:
        st.chat_message("user").write(user_query)
        with st.chat_message("assistant"):
            with st.spinner("Searching document & generating answer..."):
                response = rag_chain.invoke(user_query)
                st.write(response)