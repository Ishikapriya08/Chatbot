import streamlit as st
import os
from PIL import Image
from docx import Document
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    st.set_page_config(page_title="ChatBot")
    with st.sidebar:
        img = Image.open("C:\\Users\\ishika.priya\\OneDrive - Accenture\\Desktop\\IP_Extra\\download.jpg")
        st.image(img, width=250)
        st.markdown("<h1 style='text-align: left;font-size: 34px;'><b>ChatBot💬</b></h1>", unsafe_allow_html=True)

        # Function to move the uploaded file to a local directory
        def move_file(file_name, file_directory):
            file_path = os.path.join(file_directory, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    st.error(f"Error: {e}")
                    return False
            try:
                os.replace(file_name, file_path)
                return True
            except Exception as e:
                st.error(f"Error: {e}")
                return False

        # Function to delete the uploaded file
        def delete_file(file_name):
            if os.path.exists(file_name):
                os.remove(file_name)
                return True
            else:
                return False

        # Browse Files
        uploaded_file = st.file_uploader("Choose a .docx file",type=["docx"])
        if uploaded_file is not None:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getvalue())
            doc=Document(uploaded_file)
            text = ""
            for para in doc.paragraphs:
                text += para.text

            # split into chunks
            char_text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
            text_chunks = char_text_splitter.split_text(text)
            
            # create embeddings with OpenAI API key
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            docsearch = FAISS.from_texts(text_chunks, embeddings) 
            llm = OpenAI() 
            chain = load_qa_chain(llm, chain_type="stuff")

        # Upload File
        if st.button("Upload File"):
            file_directory = "C:\\Users\\ishika.priya\\OneDrive - Accenture\\Desktop\\IP_Extra"
            if move_file(uploaded_file.name, file_directory):
                st.success("File uploaded successfully!")
            else:
                st.error("File can't be uploaded.")

        # Delete Knowledge
        if st.button("Delete Knowledge"):
            if delete_file(uploaded_file.name):
                st.success("File deleted successfully!")
            else:
                st.error("File not found or couldn't be deleted.")

    #QnA
    st.markdown("<h1 style='text-align: center;'>What invites exploration? Questions!</h1>", unsafe_allow_html=True)
    query = st.text_input("Ask a Question")
    if st.button("Submit"):
        if query:
            docs = docsearch.similarity_search(query)
            response = chain.run(input_documents=docs, question=query)
            st.write(response)
        else:
            st.error("Please enter a question!")

if __name__ == '__main__':
    main()