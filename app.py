import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf):
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 5) 

    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    answer = [response["output_text"]]
    st.write("Reply: ", answer[0])

    return answer

def main():
    st.set_page_config(page_title="ChatPDF")
    st.header("Chat with PDF using Gemini💁")

    # Initialize session state for pdf_texts
    if 'pdf_texts' not in st.session_state:
        st.session_state['pdf_texts'] = {}

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    # Process each PDF and store the text in session state
                    for pdf in pdf_docs:
                        st.session_state['pdf_texts'][pdf.name] = get_pdf_text(pdf)
                    st.success("Done")
            else:
                st.warning("Please upload at least one PDF file.")

    # Add a section for summary with selection
    if st.session_state['pdf_texts']:
        with st.expander("PDF Summary"):
            # Create a dropdown menu to select the PDF file
            selected_pdf = st.selectbox("Select a PDF to summarize", list(st.session_state['pdf_texts'].keys()))

            if selected_pdf:
                # Get the text of the selected PDF from session state
                raw_text = st.session_state['pdf_texts'][selected_pdf]
                st.write(f"Summary of {selected_pdf}:")

                # Generate the summary of the selected PDF
                summarized_text = summarize_text(raw_text)
                st.write(summarized_text)

if __name__ == "__main__":
    main()
