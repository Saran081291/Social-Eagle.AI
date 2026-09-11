"""
CAIE Course Program - Assignment 6: Build a RAG App
Streamlit + LangChain RAG app: upload a PDF, build a FAISS vector
database from it, and ask questions answered by an OpenAI model
grounded in the PDF's content.
"""

import os
import tempfile

import streamlit as st

from dotenv import find_dotenv, load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

from langchain_classic.chains import RetrievalQA

# Automatically find and load a .env file, even if it lives in a parent
# folder (e.g. this script is nested under Day10/Assignment but .env is
# at the project root). find_dotenv() walks upward from the current
# working directory until it finds one.
load_dotenv(find_dotenv())


# ---------------------------------------------------------
# Streamlit Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄"
)

st.title("📄 RAG PDF Assistant")
st.write("Upload a PDF and ask questions about its content.")


# ---------------------------------------------------------
# API key check (fail fast, never hard-code the key)
# ---------------------------------------------------------

if not os.environ.get("OPENAI_API_KEY"):
    st.error(
        "OPENAI_API_KEY environment variable is not set. "
        "Set it before running the app, e.g.:\n\n"
        "  export OPENAI_API_KEY=\"your-key\"   # macOS/Linux\n"
        "  set OPENAI_API_KEY=your-key          # Windows cmd\n"
        "  $env:OPENAI_API_KEY=\"your-key\"      # Windows PowerShell"
    )
    st.stop()


# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "processed_file_id" not in st.session_state:
    st.session_state.processed_file_id = None


# ---------------------------------------------------------
# Load LLM only once (cached across reruns)
# ---------------------------------------------------------

@st.cache_resource
def load_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
    )


# ---------------------------------------------------------
# PDF Upload
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


# ---------------------------------------------------------
# Process PDF (only when a NEW file is uploaded)
# ---------------------------------------------------------

if uploaded_file:

    # A stable identity for "this exact upload" - name + size is enough
    # to detect a genuinely new file without hashing the whole content.
    current_file_id = f"{uploaded_file.name}-{uploaded_file.size}"

    # Skip reprocessing if this is the same file as last time. Without
    # this check, every keystroke in the question box below triggers a
    # Streamlit rerun, which would re-parse, re-chunk, and re-embed the
    # entire PDF on every single character typed.
    if current_file_id != st.session_state.processed_file_id:

        with st.spinner("Processing PDF..."):

            # Save uploaded PDF temporarily so PyPDFLoader can read it
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(uploaded_file.read())
                pdf_path = tmp_file.name

            # -------------------------------------------------
            # Load PDF
            # -------------------------------------------------

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            # Clean up the temp file now that it's loaded
            os.remove(pdf_path)

            # -------------------------------------------------
            # Split PDF text into chunks
            # -------------------------------------------------

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = text_splitter.split_documents(documents)

            # -------------------------------------------------
            # Handle PDFs with no extractable text (e.g. scanned
            # image-only pages) before touching the vector store.
            # -------------------------------------------------

            if not chunks:
                st.error(
                    "No readable text was found in this PDF. "
                    "It may be a scanned/image-only document - try a "
                    "different file, or run OCR on it first."
                )
                st.session_state.vector_db = None
                st.session_state.processed_file_id = None
                st.stop()

            # -------------------------------------------------
            # OpenAI Embeddings
            # -------------------------------------------------

            embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

            # -------------------------------------------------
            # Create FAISS Vector Database
            # -------------------------------------------------

            vector_db = FAISS.from_documents(chunks, embeddings)

            # Store vector DB and mark this file as processed
            st.session_state.vector_db = vector_db
            st.session_state.processed_file_id = current_file_id

        st.success(f"PDF processed successfully ✅ ({len(chunks)} chunks)")

    else:
        st.info("This PDF was already processed - using the existing vector database.")


# ---------------------------------------------------------
# Question Answering
# ---------------------------------------------------------

if st.session_state.vector_db is not None:

    st.divider()

    question = st.text_input(
        "Ask a question about the PDF"
    )

    if question:

        with st.spinner("Generating answer..."):

            # -------------------------------------------------
            # Retriever
            # -------------------------------------------------

            retriever = st.session_state.vector_db.as_retriever(
                search_kwargs={"k": 3}
            )

            # -------------------------------------------------
            # Load LLM
            # -------------------------------------------------

            llm = load_llm()

            # -------------------------------------------------
            # Create RAG Chain
            # -------------------------------------------------

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                chain_type="stuff"
            )

            # -------------------------------------------------
            # Generate Answer
            # -------------------------------------------------

            result = qa_chain.invoke({"query": question})

            # -------------------------------------------------
            # Display Answer
            # -------------------------------------------------

            st.subheader("Answer")
            st.write(result["result"])